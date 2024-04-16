import { useState } from 'react';
import { Modal, Row, Col, Button, Card, ListGroup, ButtonGroup } from 'react-bootstrap';

const Node = ({ nodeData, onNodeClick }) => (
  <Button
    variant="outline-primary"
    className="d-flex flex-column align-items-center p-2"
    onClick={onNodeClick}
    style={{ width: '10rem', height: '6rem' }}
  >
    <span>Node {nodeData.id}</span>
    <small>
      Temperature: {nodeData.temperature}
      <br />
      Humidity: {nodeData.humidity}
    </small>
  </Button>
);
const HistoryDataComponent = ({ nodeData }) => {
  return <div> history... </div>
}


function FactoryView({ nodeArray }) {
  const [selectedNodeIndex, setSelectedNodeIndex] = useState(null);

  const handleNodeClick = (index) => {
    setSelectedNodeIndex(index);
  };

  return (
    <>
      <h2 className="text-center">工厂平面图</h2>
      <Row className='g-2'>
        {nodeArray.map((node, index) => (
          <Col key={index}>
            <Node
              nodeData={node}
              onNodeClick={() => handleNodeClick(index)}
            />
          </Col>
        ))}
      </Row>
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