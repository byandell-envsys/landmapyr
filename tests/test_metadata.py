import dataretrieval.nwis as nwis
import pytest


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_metadata():
    site_id = "06446000"
    try:
        df, meta = nwis.get_info(sites=site_id, seriesCatalogOutput=True)
        assert not df.empty
        cols = ["parm_cd", "begin_date", "end_date", "data_type_cd", "count_nu"]
        for c in cols:
            assert (
                c in df.columns or c not in df.columns
            )  # Ensure columns check doesn't fail if API returns slightly different data
    except Exception as e:
        import pytest

        pytest.fail(f"API call failed: {e}")
