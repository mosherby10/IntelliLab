import React, { useState } from 'react';
import { askQA } from '../api';

export default function Dashboard({ token }) {
  const [question, setQuestion] = useState('');
  const [context, setContext] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleAsk(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await askQA(token, question, context);
      setAnswer(res.answer);
    } catch (err) {
      setAnswer('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Dashboard — NLP QA</h2>
      <form onSubmit={handleAsk}>
        <div>
          <label>Context (paste lecture notes)</label><br />
          <textarea value={context} onChange={e => setContext(e.target.value)} rows={6} cols={60} />
        </div>
        <div>
          <label>Question</label><br />
          <input value={question} onChange={e => setQuestion(e.target.value)} size={60} />
        </div>
        <button type="submit" disabled={loading}>Ask</button>
      </form>

      {loading && <div>Loading...</div>}
      {answer && <div><h3>Answer</h3><div>{answer}</div></div>}
    </div>
  );
}
