import React, { useEffect, useState } from "react";
import axios from "axios";
import FactoryView from "./FactoryView";
import LineChartView from "./LineChart";
import SwitchView from './SwitchView'
import "./App.css";
import 'bootstrap/dist/css/bootstrap.min.css';

export default function FactoryDashboard() {
  const [nodesData, setNodesData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1/all_sensor_data');
        setNodesData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }

    fetchData();
  });


  return (
    <div className="dashboard">
      <h1 className="text-center my-4">工厂温湿度监测系统</h1>
      <div className="row">
        <div className="col-md-4">
          <div className="card">
            <div className="card-body">
              <FactoryView nodeArray={nodesData} />
            </div>
          </div>
        </div>
        <div className="col-md-2">
          <div className="card">
            <div className="card-body">
              <SwitchView />
            </div>
          </div>
        </div>
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <LineChartView nodeArray={nodesData} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
