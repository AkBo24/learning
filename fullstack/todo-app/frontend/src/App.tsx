import React, { useState } from 'react';
import { useAddTodoMutation, useGetTodosQuery } from './api/apiSlice';
import Todo from './components/Todo';

const App = () => {
    const { data: todos } = useGetTodosQuery(undefined);
    const [addTodo, result] = useAddTodoMutation();

    const [todoTitle, setTodoTitle] = useState<string>('');
    const [todoDescription, setTodoDescription] = useState<string>('');

    const handleAddTodo = async () => {
        if (!todoTitle) {
            alert('Enter todo title');
            return;
        }
        const newTodo: Todo = {
            title: todoTitle,
            description: todoDescription,
            completed: false,
        };
        await addTodo(newTodo);
    };

    return (
        <div>
            <h1>Todos</h1>

            <form onSubmit={handleAddTodo}>
                <div>
                    <label htmlFor='new-todo-title'>Title</label>
                    <input
                        onChange={(e) => setTodoTitle(e.target.value)}
                        id='new-todo-title'
                        value={todoTitle}
                        placeholder='Enter new todo…'
                    />
                </div>

                <div>
                    <label htmlFor='new-todo-description'>Description</label>
                    <textarea
                        onChange={(e) => setTodoDescription(e.target.value)}
                        id='new-todo-description'
                        value={todoDescription}
                        placeholder='Enter todo details'
                    />
                </div>
                <button type='submit'>Add todo</button>
            </form>

            {todos?.map((todo, i) => (
                <ul key={i}>
                    <li>
                        <Todo todo={todo} />
                    </li>
                </ul>
            ))}
        </div>
    );
};

export default App;
