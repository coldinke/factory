import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import FactoryView from "./FactoryView";
import LineChartView from "./LineChart";
import HeatmapView from "./HeatChart";

import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";

export default function FactoryDashboard() {
  const [nodesData, setNodesData] = useState([]);
  const intervalRef = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/all_sensor_data"
        );
        setNodesData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
    intervalRef.current = setInterval(fetchData, 10000);

    console.log(nodesData);

    return () => clearInterval(intervalRef.current);
  }, []);

  return (
    <div className="dashboard">
      <h2 className="text-center my-4" style={{ backgroundColor: "white" }}>
        药品仓储环境温湿度监测系统
      </h2>
      <div className="row">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <FactoryView nodeArray={nodesData} />
            </div>
          </div>
        </div>
        <div className="col-md-6">
        <div className="card">
          <div className="card-body">
            <LineChartView nodeArray={nodesData} />
          </div>
            <HeatmapView nodeArray={nodesData} />
        </div>
      </div>
      </div>
    </div>
  );
}
