import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import Todo from '../components/Todo';
import { getCsrfToken } from '../utils/csrf';

export const api = createApi({
    reducerPath: 'api',
    baseQuery: fetchBaseQuery({
        baseUrl: 'http://localhost:8000',
        prepareHeaders: (headers) => {
            const csrfToken = getCsrfToken();
            if (csrfToken) {
                headers.set('X-CSRFToken', csrfToken);
            }
            return headers;
        },
    }),
    tagTypes: ['todos'],
    endpoints: (builder) => ({
        getTodos: builder.query<Todo[], undefined>({
            query: () => `/todos`,
            providesTags: ['todos'],
        }),
        addTodo: builder.mutation<Todo, Todo>({
            query: (todo) => ({
                url: `/todos/`,
                method: 'POST',
                body: todo,
            }),
            invalidatesTags: ['todos'],
        }),
        updateTodo: builder.mutation<Todo, Partial<Todo> & Pick<Todo, 'id'>>({
            query: ({ id, ...patch }) => ({
                url: `/todos/${id}/`,
                method: 'PATCH',
                body: patch,
            }),
            invalidatesTags: ['todos'],
        }),
        deleteTodo: builder.mutation<null, { id: number }>({
            query: ({ id }) => ({
                url: `/todos/${id}/`,
                method: 'DELETE',
            }),
            invalidatesTags: ['todos'],
        }),
    }),
});

export const {
    useGetTodosQuery,
    useAddTodoMutation,
    useUpdateTodoMutation,
    useDeleteTodoMutation,
} = api;
