import React, { useState } from "react";
import { OverlayTrigger, Tooltip, Button, ListGroup } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface Action {
  action: string;
  link: string;


}

interface SocialMediaActionButtonProps {
  actions: Action[];
  label:string
  icon:any;
}

const SocialMediaActionButton: React.FC<SocialMediaActionButtonProps> = ({ actions,label,icon }) => {
  const [show, setShow] = useState(false);

  return (
    <OverlayTrigger
      trigger="click"
      placement="right"
      overlay={
        <Tooltip id="tooltip-actions">
          <ListGroup variant="flush">
            {actions.map((item, index) => (
              <ListGroup.Item key={index} action href={item.link}>
                {item.action}
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Tooltip>
      }
      show={show}
      onToggle={(isOpen) => setShow(isOpen)}
    >
      <Button variant="primary" size="sm" onClick={() => setShow(!show)}>
     <FontAwesomeIcon icon ={icon}/>
       {label}
      </Button>
    </OverlayTrigger>
  );
};

export default SocialMediaActionButton;
