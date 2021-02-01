import logging
from unittest.mock import Mock

import pytest
from ophyd.sim import make_fake_device
import numpy as np

from pcdsdevices.lodcm import (H1N, LODCM, Dectris, Diode, Foil, YagLom, Y1,
                               CHI1, Y2, CHI2, H2N, SimFirstTower,
                               SimSecondTower, SimLODCMEnergyC,
                               SimLODCMEnergySi)

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def fake_lodcm():
    FakeLODCM = make_fake_device(LODCM)
    lodcm = FakeLODCM('FAKE:LOM', name='fake_lom')
    lodcm.h1n_state.state.sim_put(1)
    lodcm.h1n_state.state.sim_set_enum_strs(['Unknown'] + H1N.states_list)
    lodcm.yag.state.sim_put(1)
    lodcm.yag.state.sim_set_enum_strs(['Unknown'] + YagLom.states_list)
    lodcm.dectris.state.sim_put(1)
    lodcm.dectris.state.sim_set_enum_strs(['Unknown'] + Dectris.states_list)
    lodcm.diode.state.sim_put(1)
    lodcm.diode.state.sim_set_enum_strs(['Unknown'] + Diode.states_list)
    lodcm.foil.state.sim_put(1)
    lodcm.foil.state.sim_set_enum_strs(['Unknown'] + Foil.states_list)
    lodcm.h1n_state.state.sim_put(1)

    # additional states for Crystal Tower 1
    lodcm.y1_state.state.sim_put(1)
    lodcm.y1_state.state.sim_set_enum_strs(
        ['Unknown'] + Y1.states_list)
    lodcm.chi1_state.state.sim_put(1)
    lodcm.chi1_state.state.sim_set_enum_strs(
        ['Unknown'] + CHI1.states_list)

    # additional states for Crystal Tower 2
    lodcm.y2_state.state.sim_put(1)
    lodcm.y2_state.state.sim_set_enum_strs(
        ['Unknown'] + Y2.states_list)
    lodcm.chi2_state.state.sim_put(1)
    lodcm.chi2_state.state.sim_set_enum_strs(
        ['Unknown'] + CHI2.states_list)
    lodcm.h2n_state.state.sim_put(1)
    lodcm.h2n_state.state.sim_set_enum_strs(
        ['Unknown'] + H2N.states_list)

    return lodcm


# Crystal Tower 1 Setup
@pytest.fixture(scope='function')
def fake_tower1():
    FakeLODCM = make_fake_device(SimFirstTower)
    tower1 = FakeLODCM('FAKE:TOWER1', name='fake_t1')

    tower1.diamond_reflection.sim_put((1, 1, 1))
    tower1.silicon_reflection.sim_put((1, 1, 1))
    # 1 = 'C'
    tower1.h1n_state.state.sim_put(1)
    tower1.h1n_state.state.sim_set_enum_strs(
        ['Unknown'] + H1N.states_list)
    tower1.y1_state.state.sim_put(1)
    tower1.y1_state.state.sim_set_enum_strs(
        ['Unknown'] + Y1.states_list)
    tower1.chi1_state.state.sim_put(1)
    tower1.chi1_state.state.sim_set_enum_strs(
        ['Unknown'] + CHI1.states_list)

    return tower1


# Crystal Tower 2 Setup
@pytest.fixture(scope='function')
def fake_tower2():
    FakeLODCM = make_fake_device(SimSecondTower)
    tower2 = FakeLODCM('FAKE:TOWER2', name='fake_t2')

    tower2.diamond_reflection.sim_put((2, 2, 2))
    tower2.silicon_reflection.sim_put((2, 2, 2))

    tower2.y2_state.state.sim_put(1)
    tower2.y2_state.state.sim_set_enum_strs(
        ['Unknown'] + Y2.states_list)
    tower2.chi2_state.state.sim_put(1)
    tower2.chi2_state.state.sim_set_enum_strs(
        ['Unknown'] + CHI2.states_list)
    tower2.h2n_state.state.sim_put(1)
    tower2.h2n_state.state.sim_set_enum_strs(
        ['Unknown'] + H2N.states_list)

    return tower2


def energy_motor_setup(motor):
    motor.tower1.h1n_state.state.sim_put(1)
    motor.tower1.y1_state.state.sim_put(1)
    motor.tower1.chi1_state.state.sim_put(1)
    motor.tower2.y2_state.state.sim_put(1)
    motor.tower2.chi2_state.state.sim_put(1)
    motor.tower2.h2n_state.state.sim_put(1)
    motor.tower1.h1n_state.state.sim_put(1)
    motor.tower1.h1n_state.state.sim_set_enum_strs(
        ['Unknown'] + H1N.states_list)
    motor.tower1.y1_state.state.sim_put(1)
    motor.tower1.y1_state.state.sim_set_enum_strs(
        ['Unknown'] + Y1.states_list)
    motor.tower1.chi1_state.state.sim_put(1)
    motor.tower1.chi1_state.state.sim_set_enum_strs(
        ['Unknown'] + CHI1.states_list)
    motor.tower2.y2_state.state.sim_put(1)
    motor.tower2.y2_state.state.sim_set_enum_strs(
        ['Unknown'] + Y2.states_list)
    motor.tower2.chi2_state.state.sim_put(1)
    motor.tower2.chi2_state.state.sim_set_enum_strs(
        ['Unknown'] + CHI2.states_list)
    motor.tower2.h2n_state.state.sim_put(1)
    motor.tower2.h2n_state.state.sim_set_enum_strs(
        ['Unknown'] + H2N.states_list)
    motor.tower1.diamond_reflection.sim_put((1, 1, 1))
    motor.tower1.silicon_reflection.sim_put((1, 1, 1))
    motor.tower2.diamond_reflection.sim_put((2, 2, 2))
    motor.tower2.silicon_reflection.sim_put((2, 2, 2))


# Energy C LODCM setup
@pytest.fixture(scope='function')
def fake_energy_c():
    FakeLODCMEnergy = make_fake_device(SimLODCMEnergyC)
    energy_c = FakeLODCMEnergy('FAKE:CALC', name='fake_lom')
    energy_motor_setup(energy_c)
    # offset of 23
    energy_c.th1_c.set_current_position(23)
    return energy_c


# Energy Si LODCM setup
@pytest.fixture(scope='function')
def fake_energy_si():
    FakeLODCMEnergy = make_fake_device(SimLODCMEnergySi)
    energy_si = FakeLODCMEnergy('FAKE:CALC', name='fake_lom')
    energy_motor_setup(energy_si)
    # offset of 23
    energy_si.th1_si.set_current_position(23)
    return energy_si


def test_lodcm_destination(fake_lodcm):
    logger.debug('test_lodcm_destination')
    lodcm = fake_lodcm
    dest = lodcm.destination
    assert isinstance(dest, list)
    for d in dest:
        assert isinstance(d, str)

    lodcm.h1n_state.move('OUT')
    assert len(lodcm.destination) == 1
    lodcm.h1n_state.move('C')
    assert len(lodcm.destination) == 2
    # Block the mono line
    lodcm.yag.move('IN')
    assert len(lodcm.destination) == 1
    lodcm.h1n_state.move('Si')
    assert len(lodcm.destination) == 0
    lodcm.yag.move('OUT')
    assert len(lodcm.destination) == 1

    # Unknown state
    lodcm.h1n_state.state.sim_put('Unknown')
    assert len(lodcm.destination) == 0


def test_lodcm_branches(fake_lodcm):
    logger.debug('test_lodcm_branches')
    lodcm = fake_lodcm
    branches = lodcm.branches
    assert isinstance(branches, list)
    for b in branches:
        assert isinstance(b, str)


def test_lodcm_remove_dia(fake_lodcm):
    logger.debug('test_lodcm_remove_dia')
    lodcm = fake_lodcm
    lodcm.yag.insert(wait=True)
    cb = Mock()
    lodcm.remove_dia(moved_cb=cb, wait=True)
    assert cb.called
    assert lodcm.yag.position == 'OUT'


def test_hutch_foils():
    FakeFoil = make_fake_device(Foil)
    assert 'Zn' in FakeFoil('XPP', name='foil').in_states
    assert 'Ge' in FakeFoil('XCS', name='foil').in_states


def test_tower1_crystal_type(fake_tower1):
    tower1 = fake_tower1
    # tower1 si: y1_state = Si, chi1_state = Si, h1n = Si or Out
    tower1.h1n_state.move('OUT')
    tower1.y1_state.move('Si')
    tower1.chi1_state.move('Si')
    assert tower1.is_silicon()
    tower1.h1n_state.move('Si')
    assert tower1.is_silicon()
    # tower1 c: y1_state = C, chi1_state = C, h1n = C or Out
    tower1.h1n_state.move('OUT')
    tower1.y1_state.move('C')
    tower1.chi1_state.move('C')
    assert tower1.is_diamond()
    tower1.h1n_state.move('C')
    assert tower1.is_diamond()


def test_tower2_crystal_type(fake_tower2):
    tower2 = fake_tower2
    # tower2 si: y2_state = Si, chi2_state = Si, h2n_state = Si
    tower2.h2n_state.move('Si')
    tower2.y2_state.move('Si')
    tower2.chi2_state.move('Si')
    assert tower2.is_silicon()
    # tower2 c: y2_state = C, chi2_state = C, h2n_state = C
    tower2.h2n_state.move('C')
    tower2.y2_state.move('C')
    tower2.chi2_state.move('C')
    assert tower2.is_diamond()


def test_get_reflection_tower1(fake_tower1):
    tower1 = fake_tower1
    res = tower1.get_reflection(as_tuple=True)
    assert res == (1, 1, 1)


def test_get_reflection_tower2(fake_tower2):
    tower2 = fake_tower2
    res = tower2.get_reflection(as_tuple=True)
    assert res == (2, 2, 2)


def test_get_reflection_lodcm(fake_energy_c):
    energy = fake_energy_c
    # as of now tower 1: (1, 1, 1), tower 2: (2, 2, 2) - do not match
    # should raise an error
    with pytest.raises(ValueError):
        energy.get_reflection(as_tuple=True, check=True)
    # Si material
    # make second tower have same reflection (1, 1, 1)
    energy.tower2.diamond_reflection.sim_put((1, 1, 1))
    energy.tower2.silicon_reflection.sim_put((1, 1, 1))
    res = energy.get_reflection(as_tuple=True)
    assert res == (1, 1, 1)


def test_calc_energy_c(fake_energy_c):
    energy = fake_energy_c
    # material should be 'C'
    # make second tower have same reflection (1, 1, 1)
    energy.tower2.diamond_reflection.sim_put((1, 1, 1))
    energy.tower2.silicon_reflection.sim_put((1, 1, 1))
    # for energy 10e3 => (17.51878596767417, 427.8469911590626)
    th, z = energy.calc_energy(energy=10e3)
    assert np.isclose(th, 17.51878596767417)
    assert np.isclose(z, 427.8469911590626)


def test_calc_energy_si(fake_energy_si):
    energy = fake_energy_si
    energy.tower2.diamond_reflection.sim_put((1, 1, 1))
    energy.tower2.silicon_reflection.sim_put((1, 1, 1))
    th, z = energy.calc_energy(energy=10e3)
    # th should be 11.402710639982848
    # z should be 713.4828146545175
    assert th == 11.402710639982848
    assert z == 713.4828146545175


def test_get_energy_c(fake_energy_c):
    energy = fake_energy_c
    # material should be 'C'
    # with offset of 23
    # motor moving at 77
    energy.th1_c.move(77)
    assert energy.th1_c.motor.position == 100
    assert energy.th1_c.pseudo_motor.position == 77
    assert energy.th1_c.user_offset.get() == 23
    # when calculating energy, the th1_c.wm() should be 100 - 23: 100
    # so calculating this:
    # length = 2 * np.sin(np.deg2rad(77)) * d_space('C', (1, 1, 1))
    # wavelength_to_energy(length) / 1000
    # Out: 3.089365078593997
    assert energy.energy.position == 3.089365078593997
    res = energy.get_energy()
    assert res == 3.089365078593997


def test_get_energy_si(fake_energy_si):
    energy = fake_energy_si
    # material should be 'Si'
    # with offset of 23
    # motor moving at 77
    energy.th1_si.move(77)
    assert energy.th1_si.motor.position == 100
    assert energy.th1_si.pseudo_motor.position == 77
    assert energy.th1_si.user_offset.get() == 23
    # when calculating energy, the th1_si.wm() should be 100 - 23: 100
    # so calculating this:
    # length = 2 * np.sin(np.deg2rad(77)) * d_space('Si', (1, 1, 1))
    # wavelength_to_energy(length) / 1000
    # Out: 2.029041362547755
    res = energy.get_energy()
    assert res == 2.029041362547755
    assert energy.energy.position == 2.029041362547755


@pytest.mark.timeout(5)
def test_lodcm_disconnected():
    LODCM('TST:LOM', name='test_lom')
