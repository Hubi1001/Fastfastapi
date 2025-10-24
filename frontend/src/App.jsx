import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Plus, Edit2, Trash2, X } from 'lucide-react';
import UserForm from './components/UserForm';
import UserTable from './components/UserTable';
import UserCard from './components/UserCard';
import './index.css';

const API_URL = 'http://localhost:8000';

function App() {
  const [users, setUsers] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'table'
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRole, setFilterRole] = useState('all');

  // Fetch users
  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/users/`);
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
      alert('Error loading users');
    } finally {
      setLoading(false);
    }
  };

  const handleAddUser = async (userData) => {
    try {
      const response = await axios.post(`${API_URL}/users/`, userData);
      setUsers([...users, response.data]);
      setShowForm(false);
      alert('✅ User added successfully!');
    } catch (error) {
      alert('❌ Error adding user: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleUpdateUser = async (id, userData) => {
    try {
      const response = await axios.put(`${API_URL}/users/${id}`, userData);
      setUsers(users.map(u => u.id === id ? response.data : u));
      setEditingId(null);
      alert('✅ User updated successfully!');
    } catch (error) {
      alert('❌ Error updating user: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleDeleteUser = async (id) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    
    try {
      await axios.delete(`${API_URL}/users/${id}`);
      setUsers(users.filter(u => u.id !== id));
      alert('✅ User deleted successfully!');
    } catch (error) {
      alert('❌ Error deleting user: ' + (error.response?.data?.detail || error.message));
    }
  };

  // Filter users
  const filteredUsers = users.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = filterRole === 'all' || user.role === filterRole;
    return matchesSearch && matchesRole;
  });

  const roles = [...new Set(users.map(u => u.role))];

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0f172a', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <header style={{ backgroundColor: '#1e293b', borderBottom: '1px solid #334155', padding: '1rem' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <img src="/vite.svg" alt="Vite Logo" style={{ width: '32px', height: '32px' }} />
            <h1 style={{ fontSize: '1.875rem', fontWeight: 'bold', color: '#0ea5e9' }}>FastAPI Users</h1>
          </div>
          <button
            onClick={() => setShowForm(true)}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
            className="btn-primary"
          >
            <Plus size={20} /> Add User
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main style={{ flex: 1, maxWidth: '1280px', margin: '0 auto', width: '100%', padding: '2rem 1rem' }}>
        {/* Form Modal */}
        {showForm && (
          <UserForm
            onSubmit={handleAddUser}
            onClose={() => setShowForm(false)}
          />
        )}

        {/* Edit Modal */}
        {editingId !== null && (
          <UserForm
            user={users.find(u => u.id === editingId)}
            onSubmit={(data) => handleUpdateUser(editingId, data)}
            onClose={() => setEditingId(null)}
            isEditing={true}
          />
        )}

        {/* Controls */}
        <div style={{ marginBottom: '2rem' }}>
          <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', marginBottom: '1rem' }}>
            {/* Search */}
            <input
              type="text"
              placeholder="🔍 Search by name or email..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ flex: 1, minWidth: '200px', maxWidth: '400px' }}
            />

            {/* Filter by Role */}
            <select
              value={filterRole}
              onChange={(e) => setFilterRole(e.target.value)}
              style={{ maxWidth: '200px' }}
            >
              <option value="all">All Roles</option>
              {roles.map(role => (
                <option key={role} value={role}>{role}</option>
              ))}
            </select>

            {/* View Mode Toggle */}
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                onClick={() => setViewMode('grid')}
                className={viewMode === 'grid' ? 'btn-primary' : 'btn-secondary'}
              >
                Grid
              </button>
              <button
                onClick={() => setViewMode('table')}
                className={viewMode === 'table' ? 'btn-primary' : 'btn-secondary'}
              >
                Table
              </button>
            </div>
          </div>

          {/* Stats */}
          <div style={{ display: 'flex', gap: '1rem', fontSize: '0.875rem', color: '#9ca3af' }}>
            <div>
              📊 Total: <span style={{ color: '#0ea5e9', fontWeight: 'bold' }}>{users.length}</span> users
            </div>
            <div>
              🔍 Showing: <span style={{ color: '#0ea5e9', fontWeight: 'bold' }}>{filteredUsers.length}</span>
            </div>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div style={{ textAlign: 'center', padding: '3rem 0' }}>
            <p style={{ color: '#9ca3af', fontSize: '1.125rem' }}>⏳ Loading users...</p>
          </div>
        )}

        {/* Empty State */}
        {!loading && filteredUsers.length === 0 && (
          <div style={{ textAlign: 'center', padding: '3rem 0' }}>
            <p style={{ color: '#9ca3af', fontSize: '1.125rem' }}>No users found</p>
            <button
              onClick={() => setShowForm(true)}
              className="btn-primary"
              style={{ marginTop: '1rem', display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}
            >
              <Plus size={20} /> Add First User
            </button>
          </div>
        )}

        {/* Users Grid */}
        {!loading && filteredUsers.length > 0 && viewMode === 'grid' && (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: '1.5rem'
          }}>
            {filteredUsers.map(user => (
              <UserCard
                key={user.id}
                user={user}
                onEdit={() => setEditingId(user.id)}
                onDelete={() => handleDeleteUser(user.id)}
              />
            ))}
          </div>
        )}

        {/* Users Table */}
        {!loading && filteredUsers.length > 0 && viewMode === 'table' && (
          <UserTable
            users={filteredUsers}
            onEdit={(id) => setEditingId(id)}
            onDelete={(id) => handleDeleteUser(id)}
          />
        )}
      </main>

      {/* Footer */}
      <footer style={{ backgroundColor: '#1e293b', borderTop: '1px solid #334155', marginTop: '4rem' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '2rem 1rem', textAlign: 'center', color: '#6b7280' }}>
          <p>FastAPI + React + Vite | PostgreSQL Database</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
