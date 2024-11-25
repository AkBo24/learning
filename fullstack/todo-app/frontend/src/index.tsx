import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

import { api } from './api/apiSlice';
import { ApiProvider } from '@reduxjs/toolkit/query/react';

const root = createRoot(document.getElementById('app')!);
root.render(
    <>
        <ApiProvider api={api}>
            <App />
        </ApiProvider>
    </>
);
