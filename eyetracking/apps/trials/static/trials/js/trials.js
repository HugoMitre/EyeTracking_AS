//Functions
var generateLineChart;

generateLineChart = function(rawPupil, smoothPupil, firstIndexBaseline, lastIndexBaseline){

    rawPupil.splice(0, 0, 'Raw data');
    smoothPupil.splice(0, 0, 'Without blinks');

    var chart = c3.generate({
            data: {
                columns: [
                    rawPupil,
                    smoothPupil
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

};
