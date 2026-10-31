import { useState } from 'react';
import api from '../api/axios';

const initialState = { name: '', email: '', subject: '', message: '' };

export default function ContactPage() {
  const [form, setForm] = useState(initialState);
  const [feedback, setFeedback] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.post('/contact/', form);
      setFeedback('Your message was sent successfully. I will get back to you soon.');
      setForm(initialState);
    } catch (error) {
      setFeedback(error.response?.data?.detail || 'Something went wrong. Please try again later.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="page-shell section-block contact-page">
      <div className="section-head">
        <p className="eyebrow">Contact</p>
        <h3>Let’s talk about your next product, app, or team need</h3>
      </div>
      <form className="contact-form" onSubmit={handleSubmit}>
        <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Your name" required />
        <input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} type="email" placeholder="Email" required />
        <input value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} placeholder="Subject" required />
        <textarea value={form.message} onChange={(e) => setForm({ ...form, message: e.target.value })} placeholder="Message" rows={6} required />
        <button className="button button-primary" disabled={submitting} type="submit">{submitting ? 'Sending...' : 'Send message'}</button>
      </form>
      {feedback && <p className="form-message">{feedback}</p>}
    </div>
  );
}
