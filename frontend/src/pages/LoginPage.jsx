import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import axiosClient from '../api/axiosClient';

function LoginPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axiosClient.post('/token/', formData);
      localStorage.setItem('accessToken', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);
      navigate('/', { replace: true });
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Tên đăng nhập hoặc mật khẩu không đúng.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="login-page">
      <section className="panel login-panel">
        <p className="eyebrow">Book manager</p>
        <h1>Đăng nhập để quản lý sách</h1>
        <p className="muted">Frontend React Vite kết nối trực tiếp backend Django REST API bằng token.</p>

        <form className="login-form" onSubmit={handleSubmit}>
          <label>
            <span>Tên đăng nhập</span>
            <input name="username" value={formData.username} onChange={handleChange} autoComplete="username" required />
          </label>

          <label>
            <span>Mật khẩu</span>
            <input
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              autoComplete="current-password"
              required
            />
          </label>

          {error ? <div className="error-box">{error}</div> : null}

          <button type="submit" disabled={loading}>
            {loading ? 'Đang đăng nhập...' : 'Đăng nhập'}
          </button>
        </form>
      </section>
    </main>
  );
}

export default LoginPage;
