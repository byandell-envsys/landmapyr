import dataretrieval.nwis as nwis
import pytest

@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_lookup():
    name = "WHITE RIVER"
    state = "SD"
    try:
        df, meta = nwis.get_info(stateCd=state)
        mask = df.station_nm.str.contains(name)
        assert not df[mask].empty
        assert 'site_no' in df.columns
    except Exception as e:
        import pytest
        pytest.fail(f"API call failed: {e}")
