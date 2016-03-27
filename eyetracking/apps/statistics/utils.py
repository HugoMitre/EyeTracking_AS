import numpy as np
import datetime
from scipy import interpolate
from ..trials.models import Trial, TrialData


class Utils():

    def get_data(self, eye_data):
        """
        Return data of eye tracking with an average of pupil
        :rtype:   dict
        :return:
        """
        pupil = []
        dates = []
        distance = []

        if eye_data.count() == 0:
            return pupil, dates

        for eye in eye_data:
            # Average of pupil
            average_sample = 0.0

            # List for left and right eye per sample
            pupil_sample = []

            # if is not blink in left eye
            if eye.left_pupil_size != 0 and eye.left_avg_x != 0 and eye.left_avg_y != 0:
                pupil_sample.append(eye.left_pupil_size)

            # if is not blink in right eye
            if eye.right_pupil_size != 0 and eye.right_avg_x != 0 and eye.right_avg_y != 0:
                pupil_sample.append(eye.right_pupil_size)

            # If there is data
            if len(pupil_sample) > 0:
                average_sample = np.average(pupil_sample)

            dates.append(eye.timestamp)
            pupil.append(average_sample)
            distance.append(eye.distance)

        return {'pupil':pupil, 'dates':dates, 'distance':distance}

    def linear_interpolation(self, data):

        # Convert array to ndarray
        data_np =  np.array(data)

        # Find positions (x) and values (y) where data is not 0
        x = np.where(data_np)
        y = [data_np[element] for element in x]

        # Convert array to ndarray
        y = np.array(y)

        # Function to interpolate
        f = interpolate.interp1d(x[0], y)

        # Interpolate values where data is 0
        x_new = np.where(data_np==0)

        # Call function
        y_new = f(x_new)

        # Replace zeros with values interpolated
        i = 0
        for x in x_new[0]:
            data[x] = y_new[0][0][i]
            i+=1

    def hampel(self, data, win_length=12, n_sigma=3):

        half_win_length = win_length/2

        for i in range(half_win_length, len(data)-half_win_length+1):
            # Calculate median
            med = np.median(data[i-half_win_length:i+half_win_length])
            # Median absolute deviation (1.4826 = consistency constant)
            mad = 1.4826 * np.median(np.abs(data[i-half_win_length:i+half_win_length] - med))
            if data[i]  > n_sigma*mad or data[i] < n_sigma*mad:
                data[i] = med

    def split_values(self, dates, pupil):
        start_date = dates[0]

        # Time for baseline
        begin_baseline = start_date + datetime.timedelta(0,7)
        end_baseline = begin_baseline + datetime.timedelta(0,2)

        baseline =[]
        last_index_baseline = 0

        i = 0
        for date in dates:
            if date > begin_baseline and date < end_baseline:
                baseline.append(pupil[i])
                last_index_baseline = i
            i+=1

        trial = pupil[last_index_baseline:]

        return baseline, trial

    def get_features(self, image_id):

        baseline_array = []
        apcps_array = []
        mpd_array = []
        mpdc_array =[]

        # Get trials with the image
        trials = Trial.objects.filter(image=image_id)

        for trial in trials:

            # Init utils
            utils = Utils()

            # Get all trial data
            eye_data = TrialData.objects.filter(trial=trial.pk)

            # Average left and right eyes
            pupil, dates = utils.get_data(eye_data)

            # Linear interpolation
            pupil = utils.linear_interpolation(pupil)

            # Split baseline and trial
            baseline_pupil, trial_pupil = utils.split_values(dates, pupil)

            # Measures
            average_baseline = sum(baseline_pupil) / len(baseline_pupil)
            baseline_array.append(average_baseline)

            pcps = [(x - average_baseline)/average_baseline for x in trial_pupil]
            apcps_array.append(sum(pcps) / len(pcps))

            mpd = sum(trial_pupil) / len(trial_pupil)
            mpd_array.append(mpd)
            mpdc_array.append(mpd - average_baseline)

        baseline = round(sum(baseline_array) / len(baseline_array), 4)
        apcps = round(sum(apcps_array) / len(apcps_array), 4)
        mpd = round(sum(mpd_array) / len(mpd_array), 4)
        mpdc = round(sum(mpdc_array) / len(mpdc_array), 4)

        return baseline, apcps, mpd, mpdc

    def remove_outliers(self, data, n_sigma=2):

        # Convert array to ndarray
        data_np =  np.array(data)
        data_new = []

        mean = np.mean(data_np)
        sd = np.std(data_np)

        # if SD is not too low
        if sd > mean*0.1:

            lower = mean - n_sigma*sd
            upper = mean + n_sigma*sd

            outlier = (data_np > upper) | (data_np < lower)

            data_np[outlier] = 0.0

            data_new = data_np.tolist()

            Utils().linear_interpolation(data_new)

        return data_new

    def remove_outliers_distance(self, data, n_sigma=2):

        # Convert array to ndarray
        data_np =  np.array(data)

        lower = 45
        upper = 75

        outlier = (data_np > upper) | (data_np < lower)

        data_np[outlier] = 0.0

        data_new = data_np.tolist()

        Utils().linear_interpolation(data_new)

        return data_new

    def data_trial(self, trial_id):

        first_index_baseline = 0
        last_index_baseline = 0

        # Init utils
        utils = Utils()

        # Get data with average of left and right eyes
        eye_data = utils.get_data(TrialData.objects.filter(trial=trial_id))

        # Save raw data in another var
        raw_pupil = eye_data['pupil'][:]
        raw_distance = eye_data['distance'][:]

        # Linear interpolation
        utils.linear_interpolation(eye_data['pupil'])

        # Remove outliers distance
        eye_data['distance'] = utils.remove_outliers_distance(eye_data['distance'])
        #eye_data['distance'] = utils.remove_outliers(eye_data['distance'])

        # Hampel filter
        utils.hampel(eye_data['pupil'])
        utils.hampel(eye_data['distance'])

        # Fixed pupil with distance
        foco = 0.5
        fixed_pupil_distance = [(((distance[1]+foco)*eye_data['pupil'][distance[0]])/foco)/100 for distance in enumerate(eye_data['distance'])]

        # Time for baseline
        start_date = eye_data['dates'][0]
        begin_baseline = start_date + datetime.timedelta(0,7)
        end_baseline = begin_baseline + datetime.timedelta(0,2)

        # Get index baseline
        i = 0
        for date in eye_data['dates']:
            if date > begin_baseline and date < end_baseline:
                # Add index first position baseline
                if first_index_baseline == 0:
                    first_index_baseline = i

                # Always save the last position
                last_index_baseline = i
            i += 1

        return {'raw_pupil':raw_pupil, 'smooth_pupil': eye_data['pupil'], 'fixed_pupil_distance': fixed_pupil_distance,
                'raw_distance':raw_distance, 'smooth_distance':eye_data['distance'],
                'first_index_baseline':first_index_baseline, 'last_index_baseline':last_index_baseline}
