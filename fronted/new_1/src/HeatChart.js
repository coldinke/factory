import React, { useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';

function convertTo2DArrayWithPositions(oneDArray) {
    return oneDArray.reduce((acc, currentValue, index) => {
      const xIndex = index % 4; // 计算列索引
      const yIndex = Math.floor(index / 4); // 计算行索引
      
      if (!acc[yIndex]) {
        acc[yIndex] = [];
      }
      
      acc[yIndex].push([xIndex, yIndex, currentValue.temperature]);
      
      return acc;
    }, []);
  }


const HeatmapView = ({ nodeArray }) => {
  const [heatmapData, setHeatmapData] = useState([]);


  useEffect(() => {
    const sensorData = convertTo2DArrayWithPositions(nodeArray);
    console.log(sensorData)

    setHeatmapData(sensorData.flat());
  }, [nodeArray]);

  return (
    <div className='h-100'>
      <div className="w-100 h-100">
        <HeatmapChart title="温度热力图" data={heatmapData} />
      </div>
    </div>
  );
};

const HeatmapChart = ({ title, data }) => {
  const chartRef = useRef(null);

    console.log(data)

  useEffect(() => {
    const myChart = echarts.init(chartRef.current);

    const option = {
      title: {
        text: title,
      },
      tooltip: {
        position: 'top',
      },
      animation: false,
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: ["A", "B", "C", "D"],
        splitArea: {
          show: true,
        },
      },
      yAxis: {
        type: 'category',
        data: ["1", "2"],
        splitArea: {
          show: true,
        },
      },
      visualMap: {
        min: 0,
        max: 30,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        top: '0', 
      },
      series: [
        {
          name: '温度数据',
          type: 'heatmap',
          data: data,
          label: {
            show: true,
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(20, 20, 20, 0.5)',
            },
          },
        },
      ],
    };

    myChart.setOption(option);
    
    return () => {
        if (myChart !== null) {
          myChart.dispose();
        }
      };
  }, [title, data]);

  return <div ref={chartRef} className="heatmap-chart" style={{ width: '100%', height: '400px' }} />;
};

export default HeatmapView;