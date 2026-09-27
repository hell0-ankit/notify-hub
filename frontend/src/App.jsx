import React, { useEffect, useState } from 'react';
import { getSettings, toggleChannel, getLogs, triggerEvent } from './api';
import { Mail, MessageSquare, Play, RefreshCw, CheckCircle2, XCircle, Edit3, Save, X } from 'lucide-react';
import axios from './api';

const triggers = ['login', 'logout', 'inactivity'];
const channels = [
  { id: 'email', label: 'Email', icon: Mail },
  { id: 'whatsapp', label: 'WhatsApp', icon: MessageSquare },
];

export default function App() {
  const [settings, setSettings] = useState([]);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dispatchStatus, setDispatchStatus] = useState('');

  // Template Editing State
  const [editingSetting, setEditingSetting] = useState(null);
  const [editSubject, setEditSubject] = useState('');
  const [editBody, setEditBody] = useState('');
  const [savingTemplate, setSavingTemplate] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [settingsRes, logsRes] = await Promise.all([getSettings(), getLogs()]);
      setSettings(settingsRes.data.results || settingsRes.data);
      setLogs(logsRes.data.results || logsRes.data);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleToggle = async (trigger, channel, currentState) => {
    try {
      await toggleChannel({
        trigger,
        channel,
        is_active: !currentState,
      });
      fetchData();
    } catch (err) {
      console.error('Toggle error:', err);
    }
  };

  const handleTestTrigger = async (trigger) => {
    setDispatchStatus(`Firing ${trigger}...`);
    try {
      const res = await triggerEvent({ trigger });
      setDispatchStatus(res.data.message || 'Trigger fired successfully!');
      fetchData();
    } catch (err) {
      setDispatchStatus('Failed to fire trigger.');
    }
  };

  const openTemplateModal = (setting) => {
    setEditingSetting(setting);
    setEditSubject(setting.template_subject || '');
    setEditBody(setting.template_body || '');
  };

  const saveTemplate = async () => {
    if (!editingSetting) return;
    setSavingTemplate(true);
    try {
      await axios.patch(`/settings/${editingSetting.id}/`, {
        template_subject: editSubject,
        template_body: editBody,
      });
      setEditingSetting(null);
      fetchData();
    } catch (err) {
      console.error('Failed to save template:', err);
    } finally {
      setSavingTemplate(false);
    }
  };

  const getSettingItem = (trigger, channel) => {
    return settings.find((s) => s.trigger === trigger && s.channel === channel);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-10">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-5 gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-white">NotifyHub Control Center</h1>
            <p className="text-slate-400 text-sm mt-1">Manage notification channels, templates, and delivery audit logs.</p>
          </div>
          <button
            onClick={fetchData}
            disabled={loading}
            className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg text-sm border border-slate-700 transition w-fit cursor-pointer"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </header>

        {/* 1. Simulate Triggers */}
        <section className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-sm">
          <h2 className="text-lg font-semibold mb-4 text-slate-200">1. Simulate System Triggers</h2>
          <div className="flex flex-wrap gap-4 items-center">
            {triggers.map((t) => (
              <button
                key={t}
                onClick={() => handleTestTrigger(t)}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 px-5 py-2.5 rounded-lg font-medium text-sm transition capitalize active:scale-95 cursor-pointer"
              >
                <Play className="w-4 h-4" /> Trigger {t}
              </button>
            ))}
            {dispatchStatus && (
              <span className="text-sm font-mono text-emerald-400 ml-2">{dispatchStatus}</span>
            )}
          </div>
        </section>

        {/* 2. Channel Matrix & Templates */}
        <section className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-sm">
          <h2 className="text-lg font-semibold mb-4 text-slate-200">2. Trigger Channel Matrix & Templates</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 text-sm">
                  <th className="py-3 px-4">Event Trigger</th>
                  {channels.map((c) => (
                    <th key={c.id} className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <c.icon className="w-4 h-4 text-slate-400" />
                        {c.label}
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {triggers.map((t) => (
                  <tr key={t} className="hover:bg-slate-800/40">
                    <td className="py-4 px-4 font-medium capitalize text-slate-300">{t}</td>
                    {channels.map((c) => {
                      const item = getSettingItem(t, c.id);
                      const active = item ? item.is_active : false;
                      return (
                        <td key={c.id} className="py-4 px-4">
                          <div className="flex items-center gap-2">
                            <button
                              onClick={() => handleToggle(t, c.id, active)}
                              className={`px-3 py-1.5 rounded-md text-xs font-semibold border transition cursor-pointer ${
                                active
                                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 hover:bg-emerald-500/20'
                                  : 'bg-slate-800 text-slate-400 border-slate-700 hover:bg-slate-700'
                              }`}
                            >
                              {active ? 'Active' : 'Disabled'}
                            </button>

                            {item && (
                              <button
                                onClick={() => openTemplateModal(item)}
                                title="Edit Template"
                                className="p-1.5 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition cursor-pointer"
                              >
                                <Edit3 className="w-3.5 h-3.5" />
                              </button>
                            )}
                          </div>
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* 3. Audit Logs */}
        <section className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-sm">
          <h2 className="text-lg font-semibold mb-4 text-slate-200">3. Delivery Audit Logs</h2>
          <div className="overflow-x-auto max-h-96">
            <table className="w-full text-left border-collapse text-sm">
              <thead className="sticky top-0 bg-slate-900 border-b border-slate-800 text-slate-400">
                <tr>
                  <th className="py-3 px-3">Status</th>
                  <th className="py-3 px-3">Event</th>
                  <th className="py-3 px-3">Channel</th>
                  <th className="py-3 px-3">Recipient</th>
                  <th className="py-3 px-3">Time</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {logs.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="py-6 text-center text-slate-500">
                      No logs found. Fire a trigger above to run deliveries.
                    </td>
                  </tr>
                ) : (
                  logs.map((log) => (
                    <tr key={log.id} className="hover:bg-slate-800/40">
                      <td className="py-3 px-3">
                        {log.status === 'success' ? (
                          <span className="flex items-center gap-1.5 text-emerald-400 text-xs">
                            <CheckCircle2 className="w-4 h-4" /> Success
                          </span>
                        ) : (
                          <span className="flex items-center gap-1.5 text-rose-400 text-xs">
                            <XCircle className="w-4 h-4" /> Failed
                          </span>
                        )}
                      </td>
                      <td className="py-3 px-3 font-medium capitalize text-slate-300">{log.trigger}</td>
                      <td className="py-3 px-3 uppercase text-xs text-slate-400">{log.channel}</td>
                      <td className="py-3 px-3 font-mono text-xs text-slate-400">{log.recipient}</td>
                      <td className="py-3 px-3 text-xs text-slate-500">
                        {new Date(log.created_at).toLocaleTimeString()}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>

      </div>

      {/* Edit Template Modal */}
      {editingSetting && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 max-w-lg w-full space-y-4 shadow-xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="font-semibold text-slate-200">
                Edit Template: <span className="capitalize text-indigo-400">{editingSetting.trigger}</span> ({editingSetting.channel.toUpperCase()})
              </h3>
              <button
                onClick={() => setEditingSetting(null)}
                className="text-slate-400 hover:text-slate-200 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {editingSetting.channel === 'email' && (
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Subject</label>
                <input
                  type="text"
                  value={editSubject}
                  onChange={(e) => setEditSubject(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
                />
              </div>
            )}

            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">
                Body Template <span className="text-slate-500">(Supports: &#123;&#123;name&#125;&#125;, &#123;&#123;time&#125;&#125;, &#123;&#123;site&#125;&#125;)</span>
              </label>
              <textarea
                rows={4}
                value={editBody}
                onChange={(e) => setEditBody(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-slate-200 focus:outline-none focus:border-indigo-500 font-mono"
              />
            </div>

            <div className="flex justify-end gap-3 pt-2">
              <button
                onClick={() => setEditingSetting(null)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-sm border border-slate-700 transition cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={saveTemplate}
                disabled={savingTemplate}
                className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm transition cursor-pointer disabled:opacity-50"
              >
                <Save className="w-4 h-4" /> {savingTemplate ? 'Saving...' : 'Save Template'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}