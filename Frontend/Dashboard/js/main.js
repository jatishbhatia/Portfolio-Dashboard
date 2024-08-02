// const chart = document.querySelector("#chart").getContext('2d');

// // create a new chart instance
// new chart(chart, {
//     type: 'line',
//     data: {
//         labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'],
//         datasets: [
//             {
//                 label: 'BTC',
//                 data: [29374, 33537, 49631, 59095, 57828, 36684, 33572, 39974, 48847, 48116, 61004],
//                 borderColor: 'red',
//                 borderWidth: 2
//             },
//             {
//                 label: 'ETH',
//                 data: [29374, 33537, 49631, 59095, 57828, 36684, 33572, 39974, 48847, 48116, 61004],
//                 borderColor: 'blue',
//                 borderWidth: 2
//             }
//         ]
//     },
//     options: {
//         responsive: true
//     }
// });


// window.onload = function () {

//         var chart = new CanvasJS.Chart("chartContainer", {
//                 animationEnabled: true,
//                 theme: "light2",
//                 title:{
//                         text: "Site Traffic"
//                 },
//                 axisX:{
//                         valueFormatString: "DD MMM",
//                         crosshair: {
//                                 enabled: true,
//                                 snapToDataPoint: true
//                         }
//                 },
//                 axisY: {
//                         title: "Number of Visits",
//                         includeZero: true,
//                         crosshair: {
//                                 enabled: true
//                         }
//                 },
//                 toolTip:{
//                         shared:true
//                 },
//                 legend:{
//                         cursor:"pointer",
//                         verticalAlign: "bottom",
//                         horizontalAlign: "left",
//                         dockInsidePlotArea: true,
//                         itemclick: toogleDataSeries
//                 },
//                 data: [{
//                         type: "line",
//                         showInLegend: true,
//                         name: "Total Visit",
//                         markerType: "square",
//                         xValueFormatString: "DD MMM, YYYY",
//                         color: "#F08080",
//                         dataPoints: [
//                                 { x: new Date(2017, 0, 3), y: 650 },
//                                 { x: new Date(2017, 0, 4), y: 700 },
//                                 { x: new Date(2017, 0, 5), y: 710 },
//                                 { x: new Date(2017, 0, 6), y: 658 },
//                                 { x: new Date(2017, 0, 7), y: 734 },
//                                 { x: new Date(2017, 0, 8), y: 963 },
//                                 { x: new Date(2017, 0, 9), y: 847 },
//                                 { x: new Date(2017, 0, 10), y: 853 },
//                                 { x: new Date(2017, 0, 11), y: 869 },
//                                 { x: new Date(2017, 0, 12), y: 943 },
//                                 { x: new Date(2017, 0, 13), y: 970 },
//                                 { x: new Date(2017, 0, 14), y: 869 },
//                                 { x: new Date(2017, 0, 15), y: 890 },
//                                 { x: new Date(2017, 0, 16), y: 930 }
//                         ]
//                 },
//                 {
//                         type: "line",
//                         showInLegend: true,
//                         name: "Unique Visit",
//                         lineDashType: "dash",
//                         dataPoints: [
//                                 { x: new Date(2017, 0, 3), y: 510 },
//                                 { x: new Date(2017, 0, 4), y: 560 },
//                                 { x: new Date(2017, 0, 5), y: 540 },
//                                 { x: new Date(2017, 0, 6), y: 558 },
//                                 { x: new Date(2017, 0, 7), y: 544 },
//                                 { x: new Date(2017, 0, 8), y: 693 },
//                                 { x: new Date(2017, 0, 9), y: 657 },
//                                 { x: new Date(2017, 0, 10), y: 663 },
//                                 { x: new Date(2017, 0, 11), y: 639 },
//                                 { x: new Date(2017, 0, 12), y: 673 },
//                                 { x: new Date(2017, 0, 13), y: 660 },
//                                 { x: new Date(2017, 0, 14), y: 562 },
//                                 { x: new Date(2017, 0, 15), y: 643 },
//                                 { x: new Date(2017, 0, 16), y: 570 }
//                         ]
//                 }]
//         });
//         chart.render();

//         function toogleDataSeries(e){
//                 if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
//                         e.dataSeries.visible = false;
//                 } else{
//                         e.dataSeries.visible = true;
//                 }
//                 chart.render();
//         }

//         }

document.addEventListener("DOMContentLoaded", function() {
        const ctx = document.getElementById('chart').getContext('2d');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'],
                datasets: [
                    {
                        label: 'BTC',
                        data: [29374, 33537, 49631, 59095, 57828, 36684, 33572, 39974, 48847, 48116, 61004],
                        borderColor: 'red',
                        borderWidth: 2,
                        fill: false
                    },
                    {
                        label: 'ETH',
                        data: [2174, 2737, 3631, 4095, 4828, 6684, 7572, 6974, 8847, 8116, 9004],
                        borderColor: 'blue',
                        borderWidth: 2,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Month'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Value'
                        }
                    }
                }
            }
        });
    });
// sho wor hide the sidebar
const menuBtn = document.querySelector('#menu-btn')
const closeBtn = document.querySelector('#close-btn')
const sidebar = document.querySelector('aside')

menuBtn.addEventListener('click', () => {
        sidebar.style.display = 'block';
})

closeBtn.addEventListener('click', () => {
        sidebar.style.display = 'none';
})

//change theme
const themeBtn = document.querySelector('.theme-btn');

themeBtn.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');

        themeBtn.querySelector('span:first-child').classList.toggle('active');
        themeBtn.querySelector('span:last-child').classList.toggle('active');
})