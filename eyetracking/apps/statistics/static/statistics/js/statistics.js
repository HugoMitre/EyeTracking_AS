//Functions
var generateLineChart;
var generateBarChart;
var changeParticipantLevels;
var getLabel;

generateLineChart = function(rawPupil, smoothPupil, fixedPupilDistance, rawDistance, smoothDistance, firstIndexBaseline, lastIndexBaseline, firstIndexSolved){
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
                    {value: lastIndexBaseline, text: 'End baseline'},
                    {value: firstIndexSolved, text: 'End trial'}
                ]
            }
        }
    });

    chart.hide(['Raw distance']);
};

generateBarChart = function(idDiv, level1, level2, level3){

    var chart = c3.generate({
        bindto: idDiv,
        data: {
            columns: [
                ['Level 1', level1],
                ['Level 2', level2],
                ['Level 3', level3]
            ],
            type: 'bar'
        }
    });

};

changeParticipantLevels = function(idSelect, url, idsCharts, idsTrialsLabels){
    $(idSelect).change(function() {
        $.get(url, {participant:this.value}, function(data) {
             generateBarChart(idsCharts[1], data[1]['apcps'], data[2]['apcps'], data[3]['apcps']);
             generateBarChart(idsCharts[2], data[1]['errors'], data[2]['errors'], data[3]['errors']);
             generateBarChart(idsCharts[3], data[1]['mpd'], data[2]['mpd'], data[3]['mpd']);
             generateBarChart(idsCharts[4], data[1]['mpdc'], data[2]['mpdc'], data[3]['mpdc']);
             generateBarChart(idsCharts[5], data[1]['peak_change'], data[2]['peak_change'], data[3]['peak_change']);
             generateBarChart(idsCharts[6], data[1]['sd'], data[2]['sd'], data[3]['sd']);

             trials_num1_str = getLabel(data[1]['trials_num'], 'trial', 'trials');
             trials_num2_str = getLabel(data[2]['trials_num'], 'trial', 'trials');
             trials_num3_str = getLabel(data[3]['trials_num'], 'trial', 'trials');

             $(idsTrialsLabels[1]).html(trials_num1_str);
             $(idsTrialsLabels[2]).html(trials_num2_str);
             $(idsTrialsLabels[3]).html(trials_num3_str);
        });
    });
};

getLabel = function(num, label_singular, label_plural){
    label = '';

    if (num == 1)
        label = '(1 '+ label_singular + ')';
    else
        label = '('+ num +' ' + label_plural +')';

    return label
};