use pyo3::prelude::*;
use pyo3::types::PyModule;
use pyo3::Bound;
use numpy::PyReadonlyArray1;

#[pyfunction]
fn ema(prices: PyReadonlyArray1<f64>, window_size: usize) -> PyResult<Vec<f64>> {
    let prices: &[f64] = prices.as_slice()?; 
    Ok(compute_ema(prices, window_size))
}

#[pyfunction]
fn sma(prices: PyReadonlyArray1<f64>, window_size: usize) -> PyResult<Vec<f64>> {
    let prices: &[f64] = prices.as_slice()?;
    Ok(compute_sma(prices, window_size))
}

#[pyfunction]
fn rsi(prices: PyReadonlyArray1<f64>, window_size: usize) -> PyResult<Vec<f64>> {
    let prices: &[f64] = prices.as_slice()?;
    Ok(compute_rsi(prices, window_size))
}

/// A Python module implemented in Rust.
#[pymodule]
fn indicators_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(ema, m)?)?;
    m.add_function(wrap_pyfunction!(sma, m)?)?;
    m.add_function(wrap_pyfunction!(rsi, m)?)?;
    Ok(())
}




/// YOUR ORIGINAL SMA (unchanged functionality)
fn compute_sma(prices: &[f64], window_size: usize) -> Vec<f64> {
    let mut means: Vec<f64> = vec![f64::NAN; window_size - 1];
    let mut i: usize = 0;
    let mut j: usize = window_size;

    while j <= prices.len() {
        let window_mean =
            prices[i..j].iter().copied().sum::<f64>() / window_size as f64;
        means.push(window_mean);

        i += 1;
        j += 1;
    }
    means
}


/// YOUR ORIGINAL EMA (unchanged functionality)
fn compute_ema(prices: &[f64], window_size: usize) -> Vec<f64> {
    let k: f64 = 2.0 / (window_size as f64 + 1.0);
    let mut emas: Vec<f64> = vec![f64::NAN; window_size - 1];

    let first_ema: f64 =
        prices[0..window_size].iter().copied().sum::<f64>() / window_size as f64;

    emas.push(first_ema);
    let mut prev_ema = first_ema;

    for price in &prices[window_size..] {
        let ema_today = prev_ema + k * (*price - prev_ema);
        emas.push(ema_today);
        prev_ema = ema_today;
    }

    emas
}

fn compute_rsi(prices: &[f64], window_size: usize) -> Vec<f64>{
    //Initialise variables
    let mut i: usize= 0;
    let mut j: usize= window_size - 1;
    let mut rsis: Vec<f64> = vec![f64::NAN; window_size - 1];
    let mut diffs: Vec<f64> = vec![];
    for k in 0..(prices.len() - 1) {
        diffs.push(prices[k + 1] - prices[k])
    }
    while j <= diffs.len() {
        //gets gains and losses for particular window
        let mut gains: Vec<f64> = vec![];
        let mut losses: Vec<f64> = vec![];
        for change in &diffs[i..j] {
            if *change >= 0.0 {
                gains.push(*change);
            }
            else {
                losses.push(*change);
            }
        }
        //get average changes
        let mut avg_gain: f64 = 0.0;
        let mut avg_loss: f64 = 0.0;
        if gains.len() > 0 {
            avg_gain = gains.iter().map(|x: &f64| *x as f64).sum::<f64>() / gains.len() as f64
        }
        if losses.len() > 0 {
            avg_loss = losses.iter().map(|x: &f64| *x as f64).sum::<f64>() / losses.len() as f64
        }
        avg_loss = avg_loss.abs();
        //calculate rsi
        let mut rs: f64 = 100.0;
        if avg_loss > 1e-12 {
            rs = avg_gain / avg_loss
        }
        let curr_rsi: f64 = 100.0 - (100.0 / (1.0 + rs));
        rsis.push(curr_rsi);

        //shift window
        i += 1;
        j += 1;
    }
    rsis
}


//---TO DEVELOP USE---
//maturin build
//pip install target/wheels/indicators_core-*.whl --force-reinstall