/*
 * C2C connector — links every Operation SEMI training site to the C2C server,
 * which saves everything to Airtable.
 *
 * Every site loads this one file:
 *   <script src="https://arcchatbot.github.io/C2C/c2c-connect.js"></script>
 *
 * >>> To connect all sites at once, paste the Render address below and push. <<<
 */
(function () {
    'use strict';

    // The C2C server on Render, e.g. 'https://c2c-training.onrender.com' (no slash at the end).
    // While empty, sites keep working but nothing is saved to Airtable.
    var API_BASE = '';

    // Pages served by the C2C server itself always talk to it directly.
    if (!API_BASE && /\.onrender\.com$/.test(location.hostname)) API_BASE = location.origin;
    API_BASE = API_BASE.replace(/\/+$/, '');

    var STUDENT_KEY = 'c2cStudent';      // shared by every site on arcchatbot.github.io
    var OUTBOX_KEY = 'c2cOutbox';        // results waiting to be sent (server asleep, offline)
    var V_PATTERN = /^V00\d{6}$/;

    function read(key) { try { return JSON.parse(localStorage.getItem(key) || 'null'); } catch (e) { return null; } }
    function write(key, value) {
        try { value == null ? localStorage.removeItem(key) : localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* storage blocked */ }
    }

    /** "v00 123-456" or "VOO123456" -> "V00123456". */
    function normalizeV(raw) {
        var v = String(raw || '').toUpperCase().replace(/[\s-]/g, '');
        if (/^V[O0]{2}/.test(v)) v = 'V00' + v.slice(3);
        return v;
    }
    function isValidV(raw) { return V_PATTERN.test(normalizeV(raw)); }
    var V_HINT = 'Enter your Student ID as V00 followed by 6 numbers, for example V00123456.';

    /** The signed-in student, shared across all C2C sites: {v, first, last} or null. */
    function student() {
        var s = read(STUDENT_KEY);
        return s && V_PATTERN.test(s.v || '') ? s : null;
    }
    function fullName(s) { s = s || student(); return s ? (s.first + ' ' + s.last).trim() : ''; }

    /** Remember a student. Pass (v, first, last) or (v, "Full Name"). */
    function rememberStudent(v, first, last) {
        v = normalizeV(v);
        if (!V_PATTERN.test(v)) return null;
        if (last === undefined) {
            var parts = String(first || '').trim().split(/\s+/);
            first = parts.shift() || '';
            last = parts.join(' ');
        }
        var s = { v: v, first: String(first || '').trim(), last: String(last || '').trim() };
        write(STUDENT_KEY, s);
        try { sessionStorage.setItem('semiIntake', JSON.stringify({ id: s.v, name: fullName(s) })); } catch (e) {}
        return s;
    }
    function forgetStudent() {
        write(STUDENT_KEY, null);
        try { sessionStorage.removeItem('semiIntake'); } catch (e) {}
    }

    function apiUrl(path) {
        path = String(path).replace(/^\/+/, '');
        return API_BASE ? API_BASE + '/' + path : path;
    }

    function send(path, body) {
        if (!API_BASE) return Promise.resolve({ ok: false, reason: 'not-connected' });
        return fetch(apiUrl(path), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
            keepalive: true
        }).then(function (res) {
            if (res.ok) return { ok: true };
            return res.json().catch(function () { return {}; }).then(function (j) {
                return { ok: false, reason: res.status >= 500 ? 'server' : 'rejected', status: res.status, message: j.detail || j.error || '' };
            });
        }, function () { return { ok: false, reason: 'network' }; });
    }

    /** Log a sign-in for a system, e.g. recordSignIn('VR Cleanroom'). */
    function recordSignIn(system, s) {
        s = s || student();
        if (!s) return Promise.resolve({ ok: false, reason: 'no-student' });
        return send('api/register', { student_id: s.v, full_name: fullName(s), system: system });
    }

    /**
     * Save a finished training to Airtable.
     *   saveResult({ system: 'VR Cleanroom', track: 'Cleanroom Gowning & ESD', score: 90 })
     * Optional: studentId and fullName (otherwise the shared signed-in student is used).
     * Resolves to {ok: true}, or {ok: false, reason, queued}. Results that fail because the server
     * is asleep or the network dropped are kept and re-sent automatically later.
     */
    function saveResult(r) {
        var s = student();
        var body = {
            student_id: normalizeV(r.studentId || (s && s.v)),
            full_name: String(r.fullName || fullName(s) || '').trim(),
            system: r.system || '',
            track: r.track,
            score: Math.max(0, Math.min(100, Number(r.score) || 0))
        };
        if (!V_PATTERN.test(body.student_id)) return Promise.resolve({ ok: false, reason: 'no-student', message: V_HINT });
        return send('api/complete-training', body).then(function (res) {
            if (!res.ok && (res.reason === 'network' || res.reason === 'server' || res.reason === 'not-connected')) {
                var box = read(OUTBOX_KEY) || [];
                box.push(body);
                write(OUTBOX_KEY, box.slice(-50));
                res.queued = true;
            }
            return res;
        });
    }

    /** Re-send results that could not be saved earlier. */
    function flushOutbox() {
        var box = read(OUTBOX_KEY) || [];
        if (!API_BASE || !box.length) return Promise.resolve(0);
        write(OUTBOX_KEY, []);
        var left = [];
        return box.reduce(function (p, body) {
            return p.then(function () {
                return send('api/complete-training', body).then(function (res) {
                    if (!res.ok && res.reason !== 'rejected') left.push(body);
                });
            });
        }, Promise.resolve()).then(function () {
            write(OUTBOX_KEY, left.concat(read(OUTBOX_KEY) || []).slice(-50));
            return box.length - left.length;
        });
    }

    window.C2C = {
        API_BASE: API_BASE,
        connected: !!API_BASE,
        V_HINT: V_HINT,
        normalizeV: normalizeV,
        isValidV: isValidV,
        student: student,
        fullName: fullName,
        rememberStudent: rememberStudent,
        forgetStudent: forgetStudent,
        apiUrl: apiUrl,
        recordSignIn: recordSignIn,
        saveResult: saveResult,
        flushOutbox: flushOutbox
    };

    if (API_BASE) setTimeout(flushOutbox, 2000);
})();
