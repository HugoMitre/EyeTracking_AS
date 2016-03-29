from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.db.models import signals, Avg, Q
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..statistics.utils import Utils
from ..participants.models import Participant
from ..images.models import Image


class Trial(models.Model):
    calibration_points = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='trials/')
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    percentage_samples = models.FloatField(blank=True, null=True)
    participant = models.ForeignKey(Participant, blank=True, null=True)
    image = models.ForeignKey(Image, blank=True, null=True)
    errors = models.IntegerField(blank=True, default='0')
    resolved = models.BooleanField(blank=True, default='')
    level = models.IntegerField(blank=True, default=1)

    def get_absolute_url(self):
        return reverse('trials:detail', args=[str(self.id)])

    def handle_uploaded_file(self, file):
        # Read file
        f = open(settings.MEDIA_ROOT + '/' + file, 'r')
        lines = f.readlines()
        f.close()

        start_gaze_data = False
        data = {}
        eye_data = []

        # Loop lines
        for i in range(len(lines)):
            line = lines[i].replace('\n','').replace('\r','').split('\t')
            length_line = len(line)

            # If exist data in the line
            if start_gaze_data == True and length_line >2:

                if 'stop_recording' in line[3]:
                    data['end_date'] = line [1]
                else:

                    eye = {'timestamp':line[0],
                           'time':line[1],
                           'fix':line[2],
                           'state':line[3],
                           'rawx':line[4],
                           'rawy':line[5],
                           'avgx':line[6],
                           'avgy':line[7],
                           'psize':line[8],
                           'Lrawx':line[9],
                           'Lrawy':line[10],
                           'Lavgx':line[11],
                           'Lavgy':line[12],
                           'Lpsize':line[13],
                           'Lpupilx':line[14],
                           'Lpupily':line[15],
                           'Rrawx':line[16],
                           'Rrawy':line[17],
                           'Ravgx':line[18],
                           'Ravgy':line[19],
                           'Rpsize':line[20],
                           'Rpupilx':line[21],
                           'Rpupily':line[22],
                           'Distance': line[23]}

                    eye_data.append(eye)

            # Get trial data
            elif line[0] == 'MSG':
                if 'Participant' in line[3]:
                    data['participant'] = line[4]
                elif 'Image' in line[3]:
                    data['image'] = line[4]
                elif 'Calibration' in line[3]:
                    data['calibration_points'] = line[4]
                elif 'Comments' in line[3]:
                    data['comments'] = line[4]
                elif 'start_recording' in line[3]:
                    data['start_date'] = line [1]
                    start_gaze_data = True

        return data, eye_data

    def get_total(self):
        return Trial.objects.count()

    def get_percentage_valid(self, total):
        valid_trials = Trial.objects.filter(percentage_samples__gte=79.99).count()

        percentage_valid = (valid_trials * 100)/total

        return round(percentage_valid, 2)

    def get_solved(self):
        return Trial.objects.filter(resolved=True).count()


class TrialFeatures(models.Model):
    baseline = models.FloatField()
    apcps = models.FloatField()
    mpd = models.FloatField()
    mpdc = models.FloatField()
    peak = models.FloatField(default=0.0)
    peak_change = models.FloatField(default=0.0)
    trial = models.ForeignKey(Trial)

    def get_totals(self, level, participant = '', search = ''):

        apcps = 0.0
        apcps_array = []
        mpd = 0.0
        mpd_array = []
        mpdc = 0.0
        mpdc_array = []
        peak = 0.0
        peak_array = []
        peak_change = 0.0
        peak_change_array = []
        trials_num = 0

        if participant:
            trials = Trial.objects.filter(level=level, participant=participant, percentage_samples__gte=79.99, resolved = True)
        else:
            trials = Trial.objects.filter(level=level, percentage_samples__gte=79.99, resolved = True)

        if search:
            trials_search = trials.filter(Q(trial__participant__first_name__contains=search) | Q(trial__participant__last_name__contains=search)
                               | Q(trial__image__original_name__contains=search))
        else:
            trials_search = trials

        trials_errors = trials.aggregate(Avg('errors'))
        errors = round(trials_errors['errors__avg'], 4) if trials_errors['errors__avg'] else 0.0

        for trial in trials_search:
            features = TrialFeatures.objects.filter(trial=trial.pk).aggregate(Avg('apcps'), Avg('mpd'), Avg('mpdc'), Avg('peak'), Avg('peak_change'))
            apcps_array.append(features['apcps__avg'])
            mpd_array.append(features['mpd__avg'])
            mpdc_array.append(features['mpdc__avg'])
            peak_array.append(features['peak__avg'])
            peak_change_array.append(features['peak_change__avg'])

        if len(apcps_array) > 0:
            apcps = round(sum(apcps_array)/len(apcps_array),4)
            mpd = round(sum(mpd_array)/len(mpd_array), 4)
            mpdc = round(sum(mpdc_array)/len(mpdc_array),4)
            peak = round(sum(peak_array)/len(peak_array), 4)
            peak_change = round(sum(peak_change_array)/len(peak_change_array), 4)
            trials_num= len(apcps_array)

        return {'apcps':apcps, 'mpd':mpd, 'mpdc':mpdc, 'errors':errors, 'peak':peak, 'peak_change':peak_change, 'trials_num':trials_num}


class TrialData(models.Model):
    timestamp = models.DateTimeField()
    time = models.IntegerField()
    fix = models.BooleanField()
    state = models.PositiveSmallIntegerField()
    raw_x = models.FloatField()
    raw_y = models.FloatField()
    avg_x = models.FloatField()
    avg_y = models.FloatField()
    pupil_size = models.FloatField()
    left_raw_x = models.FloatField()
    left_raw_y = models.FloatField()
    left_avg_x = models.FloatField()
    left_avg_y = models.FloatField()
    left_pupil_size = models.FloatField()
    left_pupil_x = models.FloatField()
    left_pupil_y = models.FloatField()
    right_raw_x = models.FloatField()
    right_raw_y = models.FloatField()
    right_avg_x = models.FloatField()
    right_avg_y = models.FloatField()
    right_pupil_size = models.FloatField()
    right_pupil_x = models.FloatField()
    right_pupil_y = models.FloatField()
    distance = models.FloatField()
    trial = models.ForeignKey(Trial)

    @classmethod
    def percentage_samples(self, trial):
        total = self.objects.filter(trial=trial).count()
        missing = self.objects.filter(left_pupil_size=0, right_pupil_size=0, trial=trial).count()

        percentage_missing = (missing * 100.00)/total
        percentage_good = 100 - percentage_missing

        return round(percentage_good, 2)

    @classmethod
    def is_float(self, value):
        try:
            float(value)
        except ValueError:
            return False
        else:
            return True

@receiver(post_save, sender=Trial)
def update_trial(sender, instance, created, **kwargs):

    if created:

        # Disconnect signal to avoid recursion
        signals.post_save.disconnect(update_trial, sender=sender)

        try:
            # Get data file
            data, eye_data = Trial().handle_uploaded_file(str(instance.file))

            # Get instances
            participant = Participant.objects.get(id=data['participant'])
            image = Image.objects.get(id=data['image'])

            with transaction.atomic():

                # Add eye data
                for eye in eye_data:

                    TrialData.objects.create(timestamp=eye['timestamp'],
                                               time=eye['time'],
                                               fix=eye['fix'],
                                               state=eye['state'],
                                               raw_x=eye['rawx'],
                                               raw_y=eye['rawy'],
                                               avg_x=eye['avgx'],
                                               avg_y=eye['avgy'],
                                               pupil_size=eye['psize'],
                                               left_raw_x=eye['Lrawx'],
                                               left_raw_y=eye['Lrawy'],
                                               left_avg_x=eye['Lavgx'],
                                               left_avg_y=eye['Lavgy'],
                                               left_pupil_size=eye['Lpsize'],
                                               left_pupil_x=eye['Lpupilx'],
                                               left_pupil_y=eye['Lpupily'],
                                               right_raw_x=eye['Rrawx'],
                                               right_raw_y=eye['Rrawy'],
                                               right_avg_x=eye['Ravgx'],
                                               right_avg_y=eye['Ravgy'],
                                               right_pupil_size=eye['Rpsize'],
                                               right_pupil_x=eye['Rpupilx'],
                                               right_pupil_y=eye['Rpupily'],
                                               distance=eye['Distance']  if TrialData().is_float(eye['Distance']) else 0.0,
                                               trial=instance)

                # Assign data
                instance.participant = participant
                instance.image = image
                instance.calibration_points = data['calibration_points']
                instance.start_date = data['start_date']
                instance.end_date = data['end_date']
                instance.comments = data['comments']
                instance.percentage_samples = TrialData.percentage_samples(instance.pk)
                instance.save()

                # Save features
                features = Utils().get_features(TrialData.objects.filter(trial=instance.pk))
                TrialFeatures.objects.create(baseline=features['baseline'],
                                             apcps=features['apcps'],
                                             mpd=features['mpd'],
                                             mpdc=features['mpdc'],
                                             peak=features['peak'],
                                             peak_change=features['peak_change'],
                                             trial=instance)
        except Exception as e:
            instance.delete()
            #print e

        # Connect signal
        signals.post_save.connect(update_trial, sender=sender)

