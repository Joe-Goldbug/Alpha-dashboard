import React from 'react';
import { Input } from 'antd';

interface MultiTokenSearchProps {
  value: string;
  onChange: (value: string) => void;
  onSearch?: (value: string) => void;
  placeholder?: string;
  style?: React.CSSProperties;
  allowClear?: boolean;
}

const MultiTokenSearch: React.FC<MultiTokenSearchProps> = ({
  value,
  onChange,
  onSearch,
  placeholder = '支持多关键词：示例 IND model31',
  style,
  allowClear = true,
}) => {
  return (
    <Input.Search
      allowClear={allowClear}
      placeholder={placeholder}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      onSearch={(v) => onSearch ? onSearch(v) : onChange(v)}
      style={style}
    />
  );
};

export default MultiTokenSearch;
