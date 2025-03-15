import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { Modal, Button, Form, Alert } from "react-bootstrap";

const API_ENDPOINTS: Record<string, string> = {
  facebook: "https://api.example.com/facebook/register",
  twitter: "https://api.example.com/twitter/register",
  instagram: "https://api.example.com/instagram/register",
};

interface CreateSocialMediaAccountProps {
  show: boolean;
  handleClose: () => void;
}

const CreateSocialMediaAccount: React.FC<CreateSocialMediaAccountProps> = ({ show, handleClose }) => {
  const {platform} = useParams<{ platform: string }>()
  const navigate = useNavigate()



  const [formData, setFormData] = useState({
    username: "",
    password: "",
    name: "",
  });

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);
  

  if (!platform ||!API_ENDPOINTS[platform]) {
    alert('wrong route')
    navigate('/')
    return null

  }

  const apiUrl = API_ENDPOINTS[platform]|| "";
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);

    if (!apiUrl) {
      setError("Invalid social media platform.");
      return;
    }

    try {
      await axios.post(apiUrl, formData);
      setSuccess(true);
      setTimeout(() => {
        handleClose(); // Close modal after success
      }, 1500);
    } catch {
      setError("Failed to create account. Please try again.");
    }
  };

  return (
    <Modal show={show} onHide={handleClose} centered>
      <Modal.Header closeButton>
        <Modal.Title>Create Account for {platform?.charAt(0).toUpperCase() + platform?.slice(1)}</Modal.Title>
      </Modal.Header>

      <Modal.Body>
        {error && <Alert variant="danger">{error}</Alert>}
        {success && <Alert variant="success">Account created successfully!</Alert>}

        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Name</Form.Label>
            <Form.Control type="text" name="name" value={formData.name} onChange={handleChange} required />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Username</Form.Label>
            <Form.Control type="text" name="username" value={formData.username} onChange={handleChange} required />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" name="password" value={formData.password} onChange={handleChange} required />
          </Form.Group>

          <Button variant="primary" type="submit">Create Account</Button>
        </Form>
      </Modal.Body>
    </Modal>
  );
};

export default CreateSocialMediaAccount;
