import React, { useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';

// 温度和湿度折线图组件
const LineChart = ({ title, data }) => {
  const chartRef = useRef(null);

  useEffect(()=> {
    var myChart = echarts.init(chartRef.current);

    var option =  {
      title: {
        title: title
      },
      xAxis: {
        type: 'time',
        data: data.map(item => new Date(item.timestamp))
      },
      yAxis: {
        type: 'value',
        name: title
      },
      series: [
        {
          data: data.map(item => item.value),
          type: 'line'
        }
      ]
    };
    myChart.setOption(option);
  
  }, title, data);

  return <div ref={chartRef} className="line-chart" style={{ width: '80%', height: '350px'}} />;
};

const LineChartView = ({ nodeArray }) => {
  const [temperatureData, setTemperatureData] = useState([]);
  const [humidityData, setHumidityData] = useState([]);

  useEffect(() => {
    // 计算温度的平均值和时间戳
    const temperatureMean = nodeArray.length > 0 ? nodeArray.reduce((acc, curr) => acc + curr.temperature, 0) / nodeArray.length : 0;
    const temperatureTimestamp = Date.now();

    // 计算湿度的平均值和时间戳
    const humidityMean = nodeArray.length > 0 ? nodeArray.reduce((acc, curr) => acc + curr.humidity, 0) / nodeArray.length : 0;
    const humidityTimestamp = Date.now();

    // 更新状态
    setTemperatureData(prevData => [...prevData, { timestamp: temperatureTimestamp, value: temperatureMean }]);
    setHumidityData(prevData => [...prevData, { timestamp: humidityTimestamp, value: humidityMean }]);
  }, [nodeArray]);

  return (
    <div className="line-chart-view">
      <div className="temperature-chart">
        <LineChart title="平均温度" data={temperatureData} />
      </div>
      <div className="humidity-chart">
        <LineChart title="平均湿度" data={humidityData} />
      </div>
    </div>
  );
};

export default LineChartView;