import { describe, it, expect } from 'vitest';

const formatDateTime = (dateTime: string): string => {
    const date = new Date(dateTime);
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    return `${day}/${month}/${year} ${hours}:${minutes}`;
};

describe('formatDateTime', () => {
    it('formats a valid date-time string correctly', () => {
        const input = '2023-11-29T14:45:00';
        const expected = '29/11/2023 14:45';
        expect(formatDateTime(input)).toBe(expected);
    });

    it('formats another valid date-time string correctly', () => {
        const input = '2024-01-01T09:05:00';
        const expected = '01/01/2024 09:05';
        expect(formatDateTime(input)).toBe(expected);
    });

    it('handles invalid date-time strings gracefully', () => {
        const input = 'invalid-date';
        expect(formatDateTime(input)).toBe('NaN/NaN/NaN NaN:NaN'); 
    });

    it('formats a date-time string without time correctly (midnight)', () => {
        const input = '2024-02-28T00:00:00';
        const expected = '28/02/2024 00:00';
        expect(formatDateTime(input)).toBe(expected);
    });
});
