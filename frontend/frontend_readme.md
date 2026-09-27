# NotifyHub - Frontend Client

A responsive, modern notification management dashboard built with **React**, **Vite**, and **Tailwind CSS**. NotifyHub provides an intuitive interface for managing multi-channel notification dispatches, customizing message templates, toggling channel matrices, and reviewing live delivery audit logs.

## Key Capabilities

* **Simulate System Triggers:** One-click simulation of user lifecycle events (`Login`, `Logout`, and `Inactivity`).
* **Channel Matrix Grid:** Toggle delivery channels on or off per trigger event:
  * **Email** (powered by Resend API)
  * **WhatsApp** (powered by Meta Graph Cloud API)
* **Interactive Template Customizer:** In-app modal for customizing subject headers and body content with dynamic context placeholders (`{{name}}`, `{{time}}`, `{{site}}`).
* **Real-Time Audit Logs:** Detailed delivery logs displaying execution status (`Success` vs. `Failed`), targeted trigger, delivery medium, recipient identifier, and timestamps.
* **Dark UI Dashboard:** Fully responsive interface styled with Tailwind CSS utility classes and Lucide React icons.

##  Architecture & Tech Stack

* **Core Library:** React 18+
* **Bundler & Tooling:** Vite
* **Linter:** Oxlint (`.oxlintrc.json`)
* **CSS Framework:** Tailwind CSS
* **Icon Set:** Lucide React
* **HTTP Client:** Axios
* **Production Hosting:** Vercel

##  Repository Structure

```text
frontend/
├── dist/                   # Production build output
├── node_modules/           # Node package dependencies
├── public/                 # Static assets & icons
├── src/
│   ├── api.js              # Axios configuration & API endpoint triggers
│   ├── App.css             # Component-specific styles
│   ├── App.jsx             # Main dashboard UI, Trigger Matrix, & Template Modal
│   ├── index.css           # Tailwind base directives and global styles
│   └── main.jsx            # React root application entry point
├── .env                    # Local environment variables
├── .gitignore              # Git ignore rules
├── .oxlintrc.json          # Oxlint configuration
├── frontend_readme.md      # Frontend documentation
├── index.html              # HTML shell root template
├── package-lock.json       # Locked dependency tree
├── package.json            # Project manifest, dependencies, and npm scripts
└── vite.config.js          # Vite configuration
```

## ⚙️ Environment Configuration

Create a `.env` file in the frontend root directory to configure the backend API target:

### Local Development (`.env`)

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/notifications
```

### Production Deployment (Vercel Project Settings)

Under **Project Settings > Environment Variables**, define:

```env
VITE_API_BASE_URL=https://notifyhub-backend-d6op.onrender.com/api/notifications
```

## Getting Started

### 1. Prerequisites

Ensure you have the following installed on your workstation:
* **Node.js**: `v18.x` or higher
* **npm** or **yarn**

### 2. Setup Dependencies

From the repository root or frontend directory:

```bash
cd frontend
npm install
```

### 3. Launch Development Server

```bash
npm run dev
```

The application will launch on `http://localhost:5173`.

### 4. Create Production Build

```bash
npm run build
```

The compiled, minified bundle will be output to the `dist/` directory.

### 5. Preview Production Build Locally

```bash
npm run preview
```

##  API Endpoints Reference

The UI interacts with the Django REST Framework backend through the following routes:

| Feature | Method | Path | Purpose |
| :--- | :--- | :--- | :--- |
| **Fetch Matrix** | `GET` | `/settings/` | Loads current channel states and stored templates |
| **Toggle Channel** | `POST` | `/settings/toggle/` | Enables or disables a channel for an event trigger |
| **Update Template** | `PATCH` | `/settings/:id/` | Saves modified subject line and template body |
| **Dispatch Event** | `POST` | `/dispatch/` | Simulates an event trigger and dispatches active alerts |
| **Fetch Logs** | `GET` | `/logs/` | Retrieves recent delivery history and error logs |

##  Deployment (Vercel)

1. Connect your GitHub repository to [Vercel](https://vercel.com/?utm_source=gemini).
2. Set the root directory to `frontend` (if inside a monorepo).
3. Set the build command to `npm run build` and output directory to `dist`.
4. Add the `VITE_API_BASE_URL` environment variable.
5. Deploy. Updates pushed to the `main` branch will automatically trigger redeployments.