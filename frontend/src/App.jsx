import React, { useEffect, useState } from 'react';
import { getSettings, toggleChannel, getLogs, triggerEvent, registerDevice } from './api';
import { Mail, MessageSquare, Bell, Play, RefreshCw, CheckCircle2, XCircle } from 'lucide-react';

const triggers = ['login', 'logout', 'inactivity'];
const channels = [
  { id: 'email', label: 'Email', icon: Mail },
  { id: 'whatsapp', label: 'WhatsApp', icon: MessageSquare },
  { id: 'web_push', label: 'Web Push', icon: Bell },
];

export default function App() {
  const [settings, setSettings] = useState([]);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dispatchStatus, setDispatchStatus] = useState('');

  // 1. OneSignal Web Push initialization and auto-registration
  useEffect(() => {
    window.OneSignalDeferred = window.OneSignalDeferred || [];
    window.OneSignalDeferred.push(async function (OneSignal) {
      await OneSignal.init({
        appId: import.meta.env.VITE_ONESIGNAL_APP_ID || "8f01089e-10ec-402d-9b71-724e4eb1d6ea",
        allowLocalhostAsSecureOrigin: true,
        notifyButton: {
          enable: true,
        },
      });

      OneSignal.User.PushSubscription.addEventListener("change", async (event) => {
        if (event.current?.id) {
          try {
            await registerDevice({ player_id: event.current.id });
            console.log("Device subscribed and registered in backend:", event.current.id);
          } catch (err) {
            console.error("Device registration error:", err);
          }
        }
      });
    });
  }, []);

  // 2. Fetch data from backend
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

  // 3. Matrix toggle
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

  // 4. Test trigger dispatch
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

  const isChannelActive = (trigger, channel) => {
    const item = settings.find((s) => s.trigger === trigger && s.channel === channel);
    return item ? item.is_active : false;
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-10">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-5 gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-white">NotifyHub Control Center</h1>
            <p className="text-slate-400 text-sm mt-1">Manage notification channels, fire simulated triggers, and inspect delivery logs.</p>
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

        {/* 2. Channel Matrix */}
        <section className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-sm">
          <h2 className="text-lg font-semibold mb-4 text-slate-200">2. Trigger Channel Matrix</h2>
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
                      const active = isChannelActive(t, c.id);
                      return (
                        <td key={c.id} className="py-4 px-4">
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
    </div>
  );
}