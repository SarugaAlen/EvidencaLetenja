import { render, screen, fireEvent, waitFor } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import EditFlightDialog from '$lib/components/ui/editFlight/editFlightDialog.svelte';
import '@testing-library/jest-dom';
import userEvent from '@testing-library/user-event';

describe('Edit Flight Dialog', () => {
  
  const mockFlight = {
    idPolet: 1,
    cas_vzleta: '01/02/2002 10:00',
    cas_pristanka: '01/02/2002 12:00',
    Pilot_idPilot: 123
  };

  it('klikne na uredi in odpre modalno okno', async () => {
    
    const onSaveMock = vi.fn();
    render(EditFlightDialog, {
      props: {
        polet: mockFlight,
        onSave: onSaveMock
      }
    });

    const editButton = screen.getByText('Uredi');
    expect(editButton).toBeInTheDocument();

    await userEvent.click(editButton);

    expect(screen.getByText('Uredi polet')).toBeInTheDocument();
  });

  it('prikaže podatke v modalnem oknu', async () => {
    const onSaveMock = vi.fn();
    render(EditFlightDialog, {
      props: {
        polet: mockFlight,
        onSave: onSaveMock
      }
    });

    await userEvent.click(screen.getByText('Uredi'));

    const pilotInput = screen.getByLabelText('Pilot ID') as HTMLInputElement;
    expect(pilotInput.value).toBe('123');

    //const secondItem = screen.findAllByTestId('#cas_pristanka_id > div:nth-child(2)');
    //expect(secondItem).toBeInTheDocument();


  });

  it('preveri, ce onSave shrani pravilne podatke', async () => {
    const onSaveMock = vi.fn();
    render(EditFlightDialog, {
      props: {
        polet: mockFlight,
        onSave: onSaveMock
      }
    });

    await userEvent.click(screen.getByText('Uredi'));

    const pilotInput = screen.getByLabelText('Pilot ID');
    await userEvent.clear(pilotInput);
    await userEvent.type(pilotInput, '456');

    await userEvent.click(screen.getByText('Shrani'));

    expect(onSaveMock).toHaveBeenCalledWith({
      idPolet: 1,
      cas_vzleta: mockFlight.cas_vzleta,
      cas_pristanka: mockFlight.cas_pristanka,
      Pilot_idPilot: 456
    });
  });
});