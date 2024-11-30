import { render, screen, fireEvent } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import '@testing-library/jest-dom';
import { ZonedDateTime  } from '@internationalized/date';
import Datepicker from '../datepicker/datepicker.svelte'; 

describe('Datepicker', () => {
  it('displays "Pick a date" when no value is set', async () => {
    render(Datepicker, { value: undefined });

    expect(screen.getByText('Pick a date')).toBeInTheDocument();
  });

  it('displays the formatted date when a value is set', async () => {
    const date = new ZonedDateTime(2023, 11, 1, 'UTC', 0);

    render(Datepicker, { value: date });

    expect(screen.getByText('November 1, 2023')).toBeInTheDocument();
  });

  it('opens the popover when clicked', async () => {
    render(Datepicker, { value: undefined });

    const button = screen.getByRole('button');

    await fireEvent.click(button);

    expect(screen.getByRole('grid')).toBeInTheDocument();
  });
});
