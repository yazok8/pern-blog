import React from 'react';

interface ContainerProps {
  children: React.ReactNode;
  className?: string;
  id?: string;
}

const Container: React.FC<ContainerProps> = ({ children, className = '', id }) => {
  return (
    <div
      id={id}
      className={`min-h-screen flex flex-col p-6 ${className}`}
    >
      {children}
    </div>
  );
};

export default Container;