import React, { useEffect, useRef } from "react";
import * as echarts from "echarts";
import "./LineChart.css";

function LineChart({ nodeData, titleStr }) {
  const chartRef = useRef(null);

  useEffect(() => {
    const chart = echarts.init(chartRef.current);

    const _y_name = (titleStr === 'temperature' ? 'temperature' : 'humidity') + ('\nmean value')
    const meanValueData = nodeData.map((item) => ({
      name: item.nodeName,
      value: [item.timestamp, item.temperature],
    }));

    const option = {
      title: {
        text: titleStr,
      },
      tooltip: {
        trigger: "axis",
      },
      xAxis: {
        type: "time",
      },
      yAxis: {
        name: _y_name,
        type: "value",
      },
      series: [
        {
          name: "meanValue",
          type: "line",
          data: meanValueData,
        }
      ],
      legend: {
        data: ["Temperature"],
        textStyle: {
          fontsize: 10,
          color: "#333",
        },
      },
    };

    chart.setOption(option);
    chart.resize({
      width: 500,
      height: 250,
    });
  }, [nodeData]);

  return <div className="line-chart" ref={chartRef}></div>;
}

function LineChartView({ nodeArray }) {
  return (
    <>
      <div className="line-chart-view">
        <div className="temperature-chart">
          <LineChart nodeData={nodeArray} titleStr={'Temperature'} />
        </div>
        <div className="humidity-chart">
          <LineChart nodeData={nodeArray} titleStr={'Humidity'}/>
        </div>
      </div>
    </>
  );
}

export default LineChartView;
