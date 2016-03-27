//Functions
var generateLineChart;

generateLineChart = function(rawPupil, smoothPupil, fixedPupilDistance, rawDistance, smoothDistance, firstIndexBaseline, lastIndexBaseline){
    // Add Legends
    rawPupil.splice(0, 0, 'Raw pupil');
    smoothPupil.splice(0, 0, 'Smooth pupil');
    fixedPupilDistance.splice(0, 0, '(Smooth + distance) pupil');
    rawDistance.splice(0, 0, 'Raw distance');
    smoothDistance.splice(0, 0, 'Smooth distance');

    var chart = c3.generate({
        data: {
            columns: [
                rawPupil,
                smoothPupil,
                rawDistance,
                smoothDistance,
                fixedPupilDistance
            ]
        },
        grid: {
            x: {
                lines: [
                    {value: firstIndexBaseline, text: 'Start baseline'},
                    {value: lastIndexBaseline, text: 'End baseline'}
                ]
            }
        }
    });

    chart.hide(['Raw distance', 'Smooth distance', '(Smooth + distance) pupil']);
};
