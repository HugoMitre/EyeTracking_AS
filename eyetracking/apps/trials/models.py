from django.core.urlresolvers import reverse
from django.db import models, IntegrityError, transaction
from django.db.models import signals
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
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
        total = self.objects.count()
        missing = self.objects.filter(left_pupil_size=0, right_pupil_size=0, trial=trial).count()

        percentage_missing = (missing * 100.00)/total
        percentage_good = 100 - percentage_missing

        return round(percentage_good, 2)

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
                                               distance=eye['Distance'],
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

        except Exception:
            instance.delete()

        # Connect signal
        signals.post_save.connect(update_trial, sender=sender)

