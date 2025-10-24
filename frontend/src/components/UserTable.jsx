import React from 'react';
import { Edit2, Trash2 } from 'lucide-react';

const UserTable = ({ users, onEdit, onDelete }) => {
  const getBadgeClass = (role) => {
    return `badge badge-${role}`;
  };

  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#1e293b', borderBottom: '1px solid #334155' }}>
            <th style={{ padding: '0.75rem 1.5rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#d1d5db' }}>
              ID
            </th>
            <th style={{ padding: '0.75rem 1.5rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#d1d5db' }}>
              Name
            </th>
            <th style={{ padding: '0.75rem 1.5rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#d1d5db' }}>
              Email
            </th>
            <th style={{ padding: '0.75rem 1.5rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#d1d5db' }}>
              Role
            </th>
            <th style={{ padding: '0.75rem 1.5rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#d1d5db' }}>
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id} style={{ borderBottom: '1px solid #334155' }}>
              <td style={{ padding: '1rem 1.5rem', fontSize: '0.875rem', color: '#9ca3af' }}>
                {user.id}
              </td>
              <td style={{ padding: '1rem 1.5rem', fontSize: '0.875rem', fontWeight: '500', color: 'white' }}>
                {user.name}
              </td>
              <td style={{ padding: '1rem 1.5rem', fontSize: '0.875rem', color: '#9ca3af' }}>
                {user.email}
              </td>
              <td style={{ padding: '1rem 1.5rem', fontSize: '0.875rem' }}>
                <span className={getBadgeClass(user.role)}>
                  {user.role}
                </span>
              </td>
              <td style={{ padding: '1rem 1.5rem', fontSize: '0.875rem', display: 'flex', gap: '0.5rem' }}>
                <button
                  onClick={() => onEdit(user.id)}
                  style={{
                    padding: '0.5rem',
                    backgroundColor: 'transparent',
                    border: 'none',
                    cursor: 'pointer',
                    color: '#0ea5e9'
                  }}
                  title="Edit user"
                >
                  <Edit2 size={16} />
                </button>
                <button
                  onClick={() => onDelete(user.id)}
                  style={{
                    padding: '0.5rem',
                    backgroundColor: 'transparent',
                    border: 'none',
                    cursor: 'pointer',
                    color: '#f87171'
                  }}
                  title="Delete user"
                >
                  <Trash2 size={16} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserTable;
