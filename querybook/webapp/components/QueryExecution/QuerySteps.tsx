import React from 'react';

import { IQueryExecution, QueryExecutionStatus } from 'const/queryExecution';
import { StepsBar } from 'ui/StepsBar/StepsBar';

export const QuerySteps: React.FunctionComponent<{
    queryExecution: IQueryExecution;
}> = ({
    queryExecution: {
        status,
        task_id: taskId,
        statement_executions: statementExecutionIds,
        total,
    },
}) => {
    let currentStep = 0;
    const steps = [
        'Send to worker',
        'Connect to engine',
        'AI Summarizing',
        'Running Query',
        'Finish',
    ];

    if (taskId != null) {
        // Celery have received the query
        currentStep++;

        if (
            statementExecutionIds != null
        ) {
            // We have connected to engine
            currentStep++;
            if(total != null && status === QueryExecutionStatus.AI_SUMMARIZING) {
                currentStep++;
            }

            if (total != null && status === QueryExecutionStatus.RUNNING) {
                currentStep++;
                steps[2] = `${steps[2]} ${statementExecutionIds.length}/${total}`;
                steps[3] = `${steps[3]} ${statementExecutionIds.length}/${total}`;
            }
        }
    }

    if (status >= 3) {
        return <StepsBar steps={steps} activeStep={4} />;
    }

    return <StepsBar steps={steps} activeStep={currentStep} />;
};
