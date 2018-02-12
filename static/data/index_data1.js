// Overall progress char
$(function(){
var dom2 = document.getElementById("testingProgress");
var myChart = echarts.init(dom2);
var app = {};
option = null;
option = {
    title : {
        text: '',
        subtext: '',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : ({d}%) {c} "
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data:['1P-232-P1','1U-481-P5','GND','U-716-P5','U-462-P3','Others']
    },
    series : [
        {
            name: '测试类型',
            type: 'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:[
                {value:335, name:'1P-232-P1'},
                {value:310, name:'1U-481-P5'},
                {value:234, name:'GND'},
                {value:135, name:'U-716-P5'},
                {value:1548, name:'U-462-P3'},
                {value:1548, name:'Others'}
            ],
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};

if (option && typeof option === "object") {
    myChart.setOption(option, true);
}

})

// High status distribution
$(function(){
var dom2 = document.getElementById("highDistribution");
var myChart = echarts.init(dom2);
var app = {};
option = null;
option = {
    title : {
        text: '',
        subtext: '',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data:['1P-232-P1','1U-481-P5','GND','U-716-P5','U-462-P3','Others']
    },
    series : [
        {
            name: '测试类型',
            type: 'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:[
                {value:335, name:'1P-232-P1'},
                {value:310, name:'1U-481-P5'},
                {value:234, name:'GND'},
                {value:135, name:'U-716-P5'},
                {value:1548, name:'U-462-P3'},
                {value:1548, name:'Others'}
            ],
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};

if (option && typeof option === "object") {
    myChart.setOption(option, true);
}

})

// Chapter status
$(function(){
var dom = document.getElementById("chapterStatus");
var myChart = echarts.init(dom);
var app = {};
option = null;
app.title = '堆叠条形图';

option = {
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    legend: {
        data:['Auto-NULL','Auto-HIGH','Auto-PASS','Manual-NULL','Manual-HIGH','Manual-PASS']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis:  {
        type: 'value'
    },
    yAxis: {
        type: 'category',
        data: ['ATA21','ATA23','ATA30','ATA33','ATA49','ATA76','ATA78']
    },
    series: [
        {
            name: 'Auto-NULL',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [320, 302, 301, 334, 390, 330, 320]
        },
        {
            name: 'Auto-HIGH',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [120, 132, 101, 134, 90, 230, 210]
        },
        {
            name: 'Auto-PASS',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [220, 182, 191, 234, 290, 330, 310]
        },
        {
            name: 'Manual-NULL',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [150, 212, 201, 154, 190, 330, 410]
        },
        {
            name: 'Manual-HIGH',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [820, 832, 901, 934, 1290, 1330, 1320]
        },
        {
            name: 'Manual-PASS',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [820, 832, 901, 934, 1290, 1330, 1320]
        }
    ]
};
if (option && typeof option === "object") {
    myChart.setOption(option, true);
}
})