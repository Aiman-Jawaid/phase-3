'use client';

import React from 'react';

interface PageTitleSectionProps {
  title?: string;
  subtitle?: string;
  actionButton?: React.ReactNode;
}

const PageTitleSection: React.FC<PageTitleSectionProps> = ({
  title = 'My Tasks',
  subtitle = 'Manage your daily activities',
  actionButton
}) => {
  return (
    <div className="flex justify-between items-center mb-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
        <p className="text-gray-600 mt-1">{subtitle}</p>
      </div>
      <div>
        {actionButton}
      </div>
    </div>
  );
};

export default PageTitleSection;