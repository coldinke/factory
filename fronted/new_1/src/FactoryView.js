import { useEffect, useState } from 'react';
import { Modal, Row, Col, Button, Card, ListGroup, ButtonGroup } from 'react-bootstrap';
import axios from 'axios';
import './FactoryView.css';


const Node = ({ nodeData, onNodeClick }) => {
  return (
    <div className="node-container text-center">
      <div className="node custom-node">
        <span>Node {nodeData.nodeno}</span>
        <br />
        <small>
        Temperature: {nodeData.temperature}°C
          <br />
        Humidity: {nodeData.humidity}%
        </small>
        <br />
        <Button onClick={onNodeClick}>View History</Button>
      </div>
    </div>
  );
};

const HistoryDataComponent = ({ nodeData }) => {
  const [historyData, setHistoryData] = useState([]);

  useEffect(() => {
    const fetchHistoryData = async() => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/sensor_data/history/${nodeData.nodeno}`)
        setHistoryData(response.data.slice(0, 10));
        console.log(response)
      } catch(error) {
        console.error('Error fetching history data:', error);
      }
    };

    fetchHistoryData();

    return () => {};
  }, [nodeData]);

  return (
    <div>
      {/* <h5>History Data for Node {nodeData.nodeno}</h5> */}
      <table className="table table-striped table-bordered">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Temperature</th>
            <th>Humidity</th>
          </tr>
        </thead>
        <tbody>
          {historyData.map((data, index) => (
            <tr key={index}>
              <td>{new Date(data.timestamp).toLocaleString()}</td>
              <td>{data.temperature}&deg;C</td>
              <td>{data.humidity}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}


function FactoryView({ nodeArray }) {
  const [selectedNodeIndex, setSelectedNodeIndex] = useState(null);

  const handleNodeClick = (index) => {
    setSelectedNodeIndex(index);
  };

  return (
    <>
      <h3 className="text-center text-primary">药品仓储环境采集节点分布图</h3>
      <div className="row row-cols-2">
        {nodeArray.map((node, index) => (
          <div key={index} className="col mb-4">
            <Node
              nodeData={node}
              onNodeClick={() => handleNodeClick(index)}
            />
          </div>
        ))}
      </div>
      <Modal
        show={selectedNodeIndex != null}
        onHide={() => setSelectedNodeIndex(null)}
      >
        <Modal.Header closeButton>
          <Modal.Title>
            Node {selectedNodeIndex !== null ? selectedNodeIndex + 1 : ''}{' '}
            History
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedNodeIndex !== null && (
            <HistoryDataComponent nodeData={nodeArray[selectedNodeIndex]} />
          )}
        </Modal.Body>
      </Modal>
    </>
  );
}

export default FactoryView;
