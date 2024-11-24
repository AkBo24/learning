import React from 'react';
import Todo from './components/Todo';

const Example = (props: { title: string; number: number }) => {
    return (
        <div>
            {props.title} {props.number}
        </div>
    );
};

const App = () => {
    return <Todo todo={{ title: 'Todo' }} />;
};

export default App;
