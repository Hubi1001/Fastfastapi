import React, { useState } from 'react';
import { X } from 'lucide-react';

const UserForm = ({ user, onSubmit, onClose, isEditing }) => {
  const [formData, setFormData] = useState(
    user || { name: '', email: '', role: 'user' }
  );
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const roles = ['admin', 'user', 'moderator', 'editor', 'manager', 'viewer', 'developer', 'tester', 'contributor'];

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }
    
    if (!formData.role) {
      newErrors.role = 'Role is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setLoading(true);
    try {
      await onSubmit(formData);
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 50
    }}>
      <div style={{
        backgroundColor: '#1e293b',
        borderRadius: '0.5rem',
        padding: '2rem',
        maxWidth: '448px',
        width: '100%',
        margin: '0 1rem',
        border: '1px solid #334155'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h2 style={{ fontSize: '1.875rem', fontWeight: 'bold', color: 'white' }}>
            {isEditing ? '✏️ Edit User' : '➕ Add New User'}
          </h2>
          <button
            onClick={onClose}
            style={{
              padding: '0.25rem',
              backgroundColor: 'transparent',
              border: 'none',
              cursor: 'pointer',
              borderRadius: '0.375rem'
            }}
          >
            <X size={24} style={{ color: '#9ca3af' }} />
          </button>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {/* Name Field */}
          <div>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#d1d5db', marginBottom: '0.5rem' }}>
              Full Name
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="John Doe"
              style={{ borderColor: errors.name ? '#ef4444' : '#334155', width: '100%' }}
            />
            {errors.name && (
              <p style={{ color: '#f87171', fontSize: '0.875rem', marginTop: '0.25rem' }}>{errors.name}</p>
            )}
          </div>

          {/* Email Field */}
          <div>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#d1d5db', marginBottom: '0.5rem' }}>
              Email Address
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="john@example.com"
              style={{ borderColor: errors.email ? '#ef4444' : '#334155', width: '100%' }}
            />
            {errors.email && (
              <p style={{ color: '#f87171', fontSize: '0.875rem', marginTop: '0.25rem' }}>{errors.email}</p>
            )}
          </div>

          {/* Role Field */}
          <div>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#d1d5db', marginBottom: '0.5rem' }}>
              Role
            </label>
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              style={{ borderColor: errors.role ? '#ef4444' : '#334155', width: '100%' }}
            >
              {roles.map(role => (
                <option key={role} value={role}>{role}</option>
              ))}
            </select>
            {errors.role && (
              <p style={{ color: '#f87171', fontSize: '0.875rem', marginTop: '0.25rem' }}>{errors.role}</p>
            )}
          </div>

          {/* Buttons */}
          <div style={{ display: 'flex', gap: '0.75rem', paddingTop: '1rem' }}>
            <button
              type="button"
              onClick={onClose}
              className="btn-secondary"
              style={{ flex: 1 }}
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-primary"
              style={{ flex: 1 }}
              disabled={loading}
            >
              {loading ? '⏳ Saving...' : isEditing ? '💾 Update' : '✅ Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserForm;
