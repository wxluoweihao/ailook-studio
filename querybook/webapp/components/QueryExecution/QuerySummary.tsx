import React, { useState, useEffect } from 'react';
import { IQueryExecution, IStatementExecution, QueryExecutionStatus } from 'const/queryExecution';
import Markdown from 'markdown-to-jsx';

export const QuerySummary: React.FunctionComponent<{
    queryExecution: IQueryExecution;
    statementExecutions: IStatementExecution[];
}> = ({ queryExecution, statementExecutions }) => {
    const combinedSummary = statementExecutions
        .map((statementExecution, index) => {
            return `${statementExecution.ai_explain}\n`;
        })
        .join('');

    const title = 'Summary from AILook';
    const body = combinedSummary;

    const [isCollapsed, setIsCollapsed] = useState(false); // Start with expanded state (false)
    const [displayText, setDisplayText] = useState('');

    const toggleCollapse = () => {
        setIsCollapsed(!isCollapsed); // Toggle the collapse state on click
    };

    useEffect(() => {
        // Set the displayText to the entire body when the tab is expanded
        if (!isCollapsed) {
            setDisplayText(body); // Show the complete text when the tab is expanded
        }
    }, [body, isCollapsed]); // Trigger when `body` or `isCollapsed` changes

    return (
        <div
            style={{
                backgroundColor: '#ffffff',
                border: '1px solid #ddd',
                borderRadius: '8px',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                marginBottom: '16px',
                fontFamily: 'Arial, sans-serif',
            }}
        >
            <div
                style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '12px 16px',
                    cursor: 'pointer',
                    borderBottom: '1px solid #eee',
                    backgroundColor: '#f7f7f7',
                    borderTopLeftRadius: '8px',
                    borderTopRightRadius: '8px',
                    transition: 'background-color 0.3s',
                }}
                onClick={toggleCollapse} // Toggle collapse when clicked
            >
                <span
                    style={{
                        fontWeight: '600',
                        fontSize: '16px',
                        color: '#333',
                    }}
                >
                    {isCollapsed ? 'Show' : 'Hide'} {title}
                </span>
                <span
                    style={{
                        fontSize: '16px',
                        color: '#888',
                    }}
                >
                    {isCollapsed ? '▼' : '▲'}
                </span>
            </div>

            {!isCollapsed && (
                <div
                    style={{
                        padding: '30px',
                        backgroundColor: '#f9f9f9',
                        borderBottomLeftRadius: '8px',
                        borderBottomRightRadius: '8px',
                        margin: '20px',
                    }}
                >
                    <Markdown>{displayText}</Markdown>
                </div>
            )}
        </div>
    );
};
