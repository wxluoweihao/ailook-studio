import { QueryExecutionStatus } from 'const/queryExecution';

export enum Status {
    success = 'success',
    warning = 'warning',
    error = 'error',
    running = 'running',
    none = 'none',
}

export const STATUS_TO_TEXT_MAPPING = {
    [QueryExecutionStatus.INITIALIZED]: 'Initializing',
    [QueryExecutionStatus.DELIVERED]: 'Received By Worker',
    [QueryExecutionStatus.AI_SUMMARIZING]: 'AI Summarizing',
    [QueryExecutionStatus.RUNNING]: 'Executing Query/Queries',
    [QueryExecutionStatus.DONE]: 'Success',
    [QueryExecutionStatus.ERROR]: 'Error',
    [QueryExecutionStatus.CANCEL]: 'Cancelled',
};

export const queryStatusToStatusIcon = {
    [QueryExecutionStatus.INITIALIZED]: Status.running,
    [QueryExecutionStatus.DELIVERED]: Status.running,
    [QueryExecutionStatus.AI_SUMMARIZING]: Status.running,
    [QueryExecutionStatus.RUNNING]: Status.running,
    [QueryExecutionStatus.DONE]: Status.success,
    [QueryExecutionStatus.ERROR]: Status.error,
    [QueryExecutionStatus.CANCEL]: Status.none,
};
