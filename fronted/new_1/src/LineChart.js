import React, { useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';

const LineChartView = ({ nodeArray }) => {
  const [averageHumidityData, setAverageHumidityData] = useState([]);

  useEffect(() => {
    const groupedData = nodeArray.reduce((acc, curr) => {
      const timestamp = new Date(curr.timestamp).toISOString().split('T')[0];
      if (!acc[timestamp]) {
        acc[timestamp] = [];
      }
      acc[timestamp].push(curr);
      return acc;
    }, {});

    const processedData = Object.entries(groupedData).map(([timestamp, nodes]) => {
      const totalHumidity = nodes.reduce((sum, node) => sum + node.humidity, 0);
      const averageHumidity = totalHumidity / nodes.length;
      return {
        timestamp: new Date(timestamp),
        humidity: averageHumidity,
      };
    });

    setAverageHumidityData(processedData);

    const dataString = JSON.stringify(processedData);
    localStorage.setItem('averageHumidityData', dataString);
  
    // 当组件重新加载时，从localStorage中读取数据
    const storedData = JSON.parse(localStorage.getItem('averageHumidityData')) || [];
    setAverageHumidityData(storedData);
  }, [nodeArray]);

  console.log(averageHumidityData);
  return (
    <div className='h-100'>
      <div className="w-100 h-100">
        <LineChart title="平均湿度" data={nodeArray} />
      </div>
    </div>
  );
};

const LineChart = ({ title, data }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    var myChart = echarts.init(chartRef.current);
    var option = {
      title: {
        text: title,
      },
      xAxis: {
        type: 'time',
      },
      yAxis: {
        type: 'value',
        name: '湿度',
      },
      series: [
        {
          data: data.map(item => [item.timestamp, item.humidity]),
          type: 'line',
          name: '平均湿度',
        },
      ],
    };

    myChart.setOption(option);
  }, [title, data]);

  return <div ref={chartRef} className="line-chart" style={{ width: '100%', height: '250px' }} />;
};


export default LineChartView;