import React from 'react';

type Todo = {
    title: string;
};

type TodoProps = {
    todo: Todo;
};
const Todo: React.FC<TodoProps> = ({ todo }: TodoProps) => {
    return <h1>{todo.title}</h1>;
};

export default Todo;
