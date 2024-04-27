import { useState } from 'react';
import Form from 'react-bootstrap/Form';

const SwitchStyles = {
  marginBottom: '1rem',
};

const Switch = ({ nodeId, onStatusChange }) => {
  const [isOn, setIsOn] = useState(false);

  const handleSwitchChange = async (event) => {
    const isChecked = event.target.checked;
    setIsOn(isChecked)

    const status = isChecked ? 'on' : 'off';
    const url = `/control/node?node_id=${nodeId}&on_off=${status}`;
    
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        onStatusChange(isChecked);
      } else {
        console.error('Failed to send MQTT message');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <Form>
      <Form.Check
        style={SwitchStyles}
        type="switch"
        id={`custom-switch-${nodeId}`}
        label={`Node ${nodeId}`}
        checked={isOn}
        onChange={handleSwitchChange}
      />
    </Form>
  );
};

const SwitchViewStyles = {
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'space-between',
  height: '100%',
};

const SwitchView = () => {
  const [nodeStatus, setNodeStatus] = useState({});

  const handleStatusChange = (nodeId, isOn) => {
    setNodeStatus((prevState) => ({
      ...prevState,
      [nodeId]: isOn,
    }));
  };

  return (
    <div style={SwitchViewStyles}>
      <Switch nodeId={1} onStatusChange={(isOn) => handleStatusChange(1, isOn)} />
      <Switch nodeId={2} onStatusChange={(isOn) => handleStatusChange(2, isOn)} />
      <Switch nodeId={3} onStatusChange={(isOn) => handleStatusChange(3, isOn)} />
      <Switch nodeId={4} onStatusChange={(isOn) => handleStatusChange(4, isOn)} />
    </div>
  );
};

export default SwitchView;

  // const nodesData = [
  //   {
  //     nodeName: "Node 1",
  //     nodeNo: 1,
  //     temperature: 25.5,
  //     humidity: 60,
  //     timestamp: "2023-04-13T10:30:00Z",
  //   },
  //   {
  //     nodeName: "Node 2",
  //     nodeNo: 2,
  //     temperature: 28.2,
  //     humidity: 55,
  //     timestamp: "2023-04-13T10:31:15Z",
  //   },
  //   {
  //     nodeName: "Node 3",
  //     nodeNo: 3,
  //     temperature: 22.8,
  //     humidity: 65,
  //     timestamp: "2023-04-13T10:32:30Z",
  //   },
  //   {
  //     nodeName: "Node 4",
  //     nodeNo: 4,
  //     temperature: 22.8,
  //     humidity: 65,
  //     timestamp: "2023-04-13T10:32:30Z",
  //   },
  //   {
  //     nodeName: "Node 5",
  //     nodeNo: 5,
  //     temperature: 22.8,
  //     humidity: 65,
  //     timestamp: "2023-04-13T10:32:30Z",
  //   },
  //   {
  //     nodeName: "Node 6",
  //     nodeNo: 6,
  //     temperature: 22.8,
  //     humidity: 65,
  //     timestamp: "2023-04-13T10:32:30Z",
  //   },
  //   {
  //     nodeName: "Node 7",
  //     nodeNo: 8,
  //     temperature: 22.8,
  //     humidity: 65,
  //     timestamp: "2023-04-13T10:32:30Z",
  //   },
  //   {
  //     nodeName: "Node 8",
  //     nodeNo: 8,
  //     temperature: 22.8,
  //     humidity: 65,
  //     timestamp: "2023-04-13T10:32:30Z",
  //   },
  // ];