const CircularSpinner = () => {
    return (
        <div style={styles.container}>
            <div style={styles.spinner}></div>
        </div>
    );
};

const styles = {
    container: {
        display: 'inline-block',
        width: 80,
        height: 80,
    },
    spinner: {
        width: '100%',
        height: '100%',
        border: '8px solid #eee',
        borderTop: '8px solid #4caf50',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite',
    },
};

// Add the keyframes via a <style> tag
const SpinnerStyle = () => (
    <style>
        {`
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `}
    </style>
);

const CircularProgressWithStyle = () => (
    <>
        <SpinnerStyle />
        <CircularSpinner />
    </>
);

export default CircularProgressWithStyle;