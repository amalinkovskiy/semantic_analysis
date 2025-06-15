"""Simple benchmark for the requirement manager."""
from requirements_manager import RequirementManager


def run_benchmark():
    rm = RequirementManager()
    rm.add_requirement('R1', 'The system shall encrypt user data for security.')
    rm.add_requirement('R2', 'Startup time should be under two seconds to improve performance.')
    rm.add_requirement('R3', 'The UI shall be intuitive for usability.')

    new_req = 'Improve security by adding two-factor authentication.'
    related = rm.integrate_new_requirement('R4', new_req)
    print('New requirement:', new_req)
    print('Related requirements:', related)
    print('Graph edges:', dict(rm.edges))


if __name__ == '__main__':
    run_benchmark()
