import Form from 'react-bootstrap/Form';

const SwitchStyles = {
  marginBottom: '1rem',
};
const Switch = () => {
  return (
    <Form>
      <Form.Check style={SwitchStyles} type="switch" id="custom-switch" label="Check this switch" />
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
  return (
    <div style={SwitchViewStyles}>
    <Switch />
    <Switch />
    <Switch />
    <Switch />
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