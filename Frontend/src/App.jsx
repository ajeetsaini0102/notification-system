import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000/api";

function App() {
  const [triggers, setTriggers] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingTemplate, setEditingTemplate] = useState(null);
  const [editForm, setEditForm] = useState({
    title: "",
    subject: "",
    body: "",
    is_enabled: true,
  });
  const [creatingTemplate, setCreatingTemplate] = useState(null);
  const [createForm, setCreateForm] = useState({
    title: "",
    subject: "",
    body: "",
    is_enabled: true,
  });

  const loadData = async () => {
    try {
      const [triggerResponse, templateResponse] = await Promise.all([
        axios.get(`${API}/triggers/`),
        axios.get(`${API}/templates/`),
      ]);

      setTriggers(triggerResponse.data);
      setTemplates(templateResponse.data);
    } catch (error) {
      console.error("API Error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const getTemplate = (triggerId, channel) => {
  const matchingTemplates = templates.filter(
    (template) =>
      template.trigger === triggerId &&
      template.channel === channel
  );

  return matchingTemplates[matchingTemplates.length - 1];
};

  const openEdit = (template) => {
    setEditingTemplate(template);

    setEditForm({
      title: template.title || "",
      subject: template.subject || "",
      body: template.body || "",
      is_enabled: template.is_enabled,
    });
  };

  const saveTemplate = async () => {
    try {
      await axios.patch(
        `${API}/templates/${editingTemplate.id}/`,
        editForm
      );

      setEditingTemplate(null);
      await loadData();

      alert("Template updated successfully!");
    } catch (error) {
      console.error("Update Error:", error);
      alert("Failed to update template");
    }
  };

  const createTemplate = async () => {
    try {
      await axios.post(`${API}/templates/`, {
        trigger: creatingTemplate.trigger,
        channel: creatingTemplate.channel,
        title: createForm.title,
        subject: createForm.subject,
        body: createForm.body,
        is_enabled: createForm.is_enabled,
      });

      setCreatingTemplate(null);
      setCreateForm({
        title: "",
        subject: "",
        body: "",
        is_enabled: true,
      });

      await loadData();

      alert("Template created successfully!");
    } catch (error) {
      console.error("Create Error:", error);
      alert("Failed to create template");
    }
  };
  const toggleTemplate = async (template) => {
    try {
      await axios.patch(
        `${API}/templates/${template.id}/`,
        {
          is_enabled: !template.is_enabled,
        }
      );

      await loadData();
    } catch (error) {
      console.error("Toggle Error:", error);
      alert("Failed to change notification status");
    }
  };

  const testTemplate = async (template) => {
    try {
      const response = await axios.post(
        `${API}/templates/${template.id}/test/`
      );

      alert(response.data.message);
    } catch (error) {
      console.error("Test Send Error:", error);

      const message =
        error.response?.data?.message || "Test notification failed";

      alert(message);
    }
  };
  const simulateEvent = async (eventName) => {
    try {
      const endpoint =
        eventName === "Login"
          ? `${API}/test-login/`
          : `${API}/test-logout/`;

      const response = await axios.post(endpoint);

      alert(response.data.message);
    } catch (error) {
      console.error("Event Error:", error);

      const message =
        error.response?.data?.message ||
        `Failed to trigger ${eventName}`;

      alert(message);
    }
  };

  if (loading) {
    return <div className="app">Loading...</div>;
  }

  return (
    <div className="app">
      <div className="header">

        <div>
          <h1>Notification Settings</h1>
          <p>Manage notification triggers and templates</p>
        </div>
      </div>
      <div className="event-tester">
        <div>
          <h2>Notification Event Tester</h2>
          <p>Test complete Login and Logout notification flows.</p>
        </div>

        <div className="event-buttons">
          <button
            className="login-btn"
            onClick={() => simulateEvent("Login")}
          >
            Simulate Login
          </button>

          <button
            className="logout-btn"
            onClick={() => simulateEvent("Logout")}
          >
            Simulate Logout
          </button>
        </div>
      </div>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Trigger</th>
              <th>WhatsApp</th>
              <th>Email</th>
              <th>Web Push</th>
            </tr>
          </thead>

          <tbody>
            {triggers.map((trigger) => {
              const whatsapp = getTemplate(trigger.id, "whatsapp");
              const email = getTemplate(trigger.id, "email");
              const webPush = getTemplate(trigger.id, "web_push");

              return (
                <tr key={trigger.id}>
                  <td>
                    <strong>{trigger.name}</strong>
                    <div className="description">
                      {trigger.description}
                    </div>
                  </td>

                  <td>
                    {whatsapp ? (
                      <div className="template">
                        <strong>{whatsapp.title || "WhatsApp Template"}</strong>
                        <p>{whatsapp.body}</p>
                        <button
                          className={`status ${whatsapp.is_enabled ? "status-on" : "status-off"}`}
                          onClick={() => toggleTemplate(whatsapp)}
                        >
                          {whatsapp.is_enabled ? "ON" : "OFF"}
                        </button>
                        <div className="actions">
                          <button
                            className="edit-btn"
                            onClick={() => openEdit(whatsapp)}
                          >
                            Edit
                          </button>
                          <button
                            className="create-btn"
                            onClick={() => {
                              setCreatingTemplate({
                                trigger: trigger.id,
                                channel: "whatsapp",
                              });
                              setCreateForm({
                                title: "",
                                subject: "",
                                body: "",
                                is_enabled: true,
                              });
                            }}
                          >
                            Create
                          </button>
                          <button
                            className="test-btn"
                            onClick={() => testTemplate(whatsapp)}
                          >
                            Test Send
                          </button>
                        </div>
                      </div>
                    ) : (
                      <button
                        className="create-btn"
                        onClick={() => {
                          setCreatingTemplate({
                            trigger: trigger.id,
                            channel: "whatsapp",
                          });
                          setCreateForm({
                            title: "",
                            subject: "",
                            body: "",
                            is_enabled: true,
                          });
                        }}
                      >
                        + Create
                      </button>
                    )}
                  </td>

                  <td>
                    {email ? (
                      <div className="template">
                        <strong>{email.title || "Email Template"}</strong>
                        <p>{email.body}</p>
                        <button
                          className={`status ${email.is_enabled ? "status-on" : "status-off"}`}
                          onClick={() => toggleTemplate(email)}
                        >
                          {email.is_enabled ? "ON" : "OFF"}
                        </button>
                        <div className="actions">
                          <button
                            className="edit-btn"
                            onClick={() => openEdit(email)}
                          >
                            Edit
                          </button>
                          <button
                            className="create-btn"
                            onClick={() => {
                              setCreatingTemplate({
                                trigger: trigger.id,
                                channel: "email",
                              });
                              setCreateForm({
                                title: "",
                                subject: "",
                                body: "",
                                is_enabled: true,
                              });
                            }}
                          >
                            Create
                          </button>
                          <button
                            className="test-btn"
                            onClick={() => testTemplate(email)}
                          >
                            Test Send
                          </button>
                        </div>
                      </div>
                    ) : (
                      <button
                        className="create-btn"
                        onClick={() => {
                          setCreatingTemplate({
                            trigger: trigger.id,
                            channel: "email",
                          });
                          setCreateForm({
                            title: "",
                            subject: "",
                            body: "",
                            is_enabled: true,
                          });
                        }}
                      >
                        + Create
                      </button>
                    )}
                  </td>

                  <td>
                    {webPush ? (
                      <div className="template">
                        <strong>{webPush.title || "Web Push Template"}</strong>
                        <p>{webPush.body}</p>
                        <button
                          className={`status ${webPush.is_enabled ? "status-on" : "status-off"}`}
                          onClick={() => toggleTemplate(webPush)}
                        >
                          {webPush.is_enabled ? "ON" : "OFF"}
                        </button>
                        <div className="actions">
                          <button
                            className="edit-btn"
                            onClick={() => openEdit(webPush)}
                          >
                            Edit
                          </button>
                          <button
                            className="create-btn"
                            onClick={() => {
                              setCreatingTemplate({
                                trigger: trigger.id,
                                channel: "web_push",
                              });
                              setCreateForm({
                                title: "",
                                subject: "",
                                body: "",
                                is_enabled: true,
                              });
                            }}
                          >
                            Create
                          </button>
                          <button
                            className="test-btn"
                            onClick={() => testTemplate(webPush)}
                          >
                            Test Send
                          </button>
                        </div>
                      </div>
                    ) : (
                      <button
                        className="create-btn"
                        onClick={() => {
                          setCreatingTemplate({
                            trigger: trigger.id,
                            channel: "web_push",
                          });
                          setCreateForm({
                            title: "",
                            subject: "",
                            body: "",
                            is_enabled: true,
                          });
                        }}
                      >
                        + Create
                      </button>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

      </div>
      {editingTemplate && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Edit Template</h2>

            <label>Title</label>
            <input
              type="text"
              value={editForm.title}
              onChange={(e) =>
                setEditForm({
                  ...editForm,
                  title: e.target.value,
                })
              }
            />

            {editingTemplate.channel === "email" && (
              <>
                <label>Subject</label>
                <input
                  type="text"
                  value={editForm.subject}
                  onChange={(e) =>
                    setEditForm({
                      ...editForm,
                      subject: e.target.value,
                    })
                  }
                />
              </>
            )}

            <label>Body</label>
            <textarea
              rows="5"
              value={editForm.body}
              onChange={(e) =>
                setEditForm({
                  ...editForm,
                  body: e.target.value,
                })
              }
            />

            <label className="checkbox-row">
              <input
                type="checkbox"
                checked={editForm.is_enabled}
                onChange={(e) =>
                  setEditForm({
                    ...editForm,
                    is_enabled: e.target.checked,
                  })
                }
              />
              Enabled
            </label>

            <div className="modal-actions">
              <button
                className="cancel-btn"
                onClick={() => setEditingTemplate(null)}
              >
                Cancel
              </button>

              <button
                className="save-btn"
                onClick={saveTemplate}
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      )}

      {creatingTemplate && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Create Template</h2>

            <label>Title</label>
            <input
              type="text"
              value={createForm.title}
              onChange={(e) =>
                setCreateForm({
                  ...createForm,
                  title: e.target.value,
                })
              }
            />

            {creatingTemplate.channel === "email" && (
              <>
                <label>Subject</label>
                <input
                  type="text"
                  value={createForm.subject}
                  onChange={(e) =>
                    setCreateForm({
                      ...createForm,
                      subject: e.target.value,
                    })
                  }
                />
              </>
            )}

            <label>Body</label>
            <textarea
              rows="5"
              value={createForm.body}
              onChange={(e) =>
                setCreateForm({
                  ...createForm,
                  body: e.target.value,
                })
              }
            />

            <label className="checkbox-row">
              <input
                type="checkbox"
                checked={createForm.is_enabled}
                onChange={(e) =>
                  setCreateForm({
                    ...createForm,
                    is_enabled: e.target.checked,
                  })
                }
              />
              Enabled
            </label>

            <div className="modal-actions">
              <button
                className="cancel-btn"
                onClick={() => setCreatingTemplate(null)}
              >
                Cancel
              </button>

              <button
                className="save-btn"
                onClick={createTemplate}
              >
                Create Template
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;