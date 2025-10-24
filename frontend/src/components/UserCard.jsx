import React from 'react';
import { Edit2, Trash2 } from 'lucide-react';

const UserCard = ({ user, onEdit, onDelete }) => {
  const getBadgeClass = (role) => {
    return `badge badge-${role}`;
  };

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
        <div>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: 'white', marginBottom: '0.5rem' }}>
            {user.name}
          </h3>
          <p style={{ color: '#9ca3af', fontSize: '0.875rem' }}>
            {user.email}
          </p>
        </div>
        <span className={getBadgeClass(user.role)}>
          {user.role}
        </span>
      </div>

      <div style={{ borderTop: '1px solid #334155', paddingTop: '1rem', marginTop: '1rem' }}>
        <div style={{ fontSize: '0.75rem', color: '#6b7280', marginBottom: '1rem' }}>
          ID: {user.id}
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            onClick={onEdit}
            style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
            className="btn-secondary"
          >
            <Edit2 size={16} /> Edit
          </button>
          <button
            onClick={onDelete}
            style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
            className="btn-danger"
          >
            <Trash2 size={16} /> Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default UserCard;
