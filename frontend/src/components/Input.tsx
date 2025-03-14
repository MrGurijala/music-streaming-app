import React from "react";

interface InputProps {
  placeholder: string;
  type?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const Input: React.FC<InputProps> = ({
  placeholder,
  type = "text",
  value,
  onChange,
}) => {
  return (
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className="border border-gray-300 px-4 py-2 rounded w-full mb-2"
    />
  );
};

export default Input;
