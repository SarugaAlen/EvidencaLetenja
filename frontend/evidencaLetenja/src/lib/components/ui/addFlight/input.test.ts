import { render, screen } from '@testing-library/svelte';
import { describe, it, expect } from 'vitest';
import '@testing-library/jest-dom';
import Input from '../input/input.svelte';

describe('Input Component', () => {
  it('renders the input with the correct initial value', () => {
    render(Input, { value: 'Testiram input dodajanja leta' });

    const input = screen.getByRole('textbox'); 
    expect(input).toHaveValue('Testiram input dodajanja leta');
  });
});
