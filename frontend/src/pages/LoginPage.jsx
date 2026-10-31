import { useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const { login, isOwner, loading } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: 'owner', password: 'admin123' });
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (loading) {
    return <div className="page-shell section-block state-card">Checking your session...</div>;
  }

  if (isOwner) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      await login(form);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to log in. Please check your credentials.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="page-shell section-block login-page">
      <div className="login-card">
        <p className="eyebrow">Owner login</p>
        <h3>Welcome back</h3>
        <form onSubmit={handleSubmit} className="login-form">
          <label>
            <span>Username</span>
            <input value={form.username} onChange={(event) => setForm({ ...form, username: event.target.value })} required />
          </label>
          <label>
            <span>Password</span>
            <input type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} required />
          </label>
          <button type="submit" className="button button-primary" disabled={submitting}>{submitting ? 'Signing in...' : 'Login'}</button>
        </form>
        {error && <p className="form-message error">{error}</p>}
      </div>
    </div>
  );
}
