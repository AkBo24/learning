import React from 'react';
import Todo from './components/Todo';
import { useAddTodoMutation, useGetTodosQuery } from './api/apiSlice';

const App = () => {
    const { data: todos } = useGetTodosQuery(undefined);
    const [addTodo, result] = useAddTodoMutation();

    console.log(todos);

    const handleAddTodo = async () => {
        const newTodo: Todo = {
            title: 'Manually added todo',
            description: 'using a button to create this todo',
            completed: false,
        };
        const t = await addTodo(newTodo);
        console.log(t);
    };

    return (
        <div>
            <h1>Todos</h1>
            <button onClick={handleAddTodo}>Add todo</button>

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
